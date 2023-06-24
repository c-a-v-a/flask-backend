import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from sqlalchemy import delete, update

from models.database import db_session
from models.bean import BeanModel, RoastEnum
from .custom_node import CustomNode


class Bean(SQLAlchemyObjectType):
    class Meta:
        model = BeanModel
        interfaces = ( CustomNode, )


class BeanQuery(graphene.ObjectType):
    all_beans = SQLAlchemyConnectionField(Bean.connection)


class AddBeanInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    roast = graphene.String(required=True)


class AddBean(graphene.Mutation):
    class Arguments:
        input = AddBeanInput(required=True)

    bean = graphene.Field(lambda: Bean)

    def mutate(self, info, input):
        input.roast = RoastEnum[input.roast]
        bean = BeanModel(**input)

        db_session.add(bean)
        db_session.commit()

        return AddBean(bean=bean)


class DeleteBean(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    id = graphene.ID()

    def mutate(self, info, id):
        query = (delete(BeanModel).where(BeanModel.id == id))
        db_session.execute(query)
        db_session.commit()

        return DeleteBean(id=id)


class UpdateBeanInput(graphene.InputObjectType):
    name = graphene.String()
    roast = graphene.String()


class UpdateBean(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        input = UpdateBeanInput(required=True)

    bean = graphene.Field(lambda: Bean)

    def mutate(self, info, id, input):
        query = (update(BeanModel).where(BeanModel.id==id).values(**input))

        db_session.execute(query)
        db_session.commit()

        bean = Bean.get_query(info).filter(BeanModel.id==id).first()

        return UpdateBean(bean=bean)


class BeanMutation(graphene.ObjectType):
    add_bean = AddBean.Field()
    delete_bean = DeleteBean.Field()
    update_bean = UpdateBean.Field()
