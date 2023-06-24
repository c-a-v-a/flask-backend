import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from sqlalchemy import delete, update

from models.database import db_session
from models.coffee_type import CoffeeTypeModel
from .custom_node import CustomNode


class CoffeeType(SQLAlchemyObjectType):
    class Meta:
        model = CoffeeTypeModel
        interfaces = ( CustomNode, )


class CoffeeTypeQuery(graphene.ObjectType):
    all_coffee_types = SQLAlchemyConnectionField(CoffeeType.connection)


class AddCoffeeTypeInput(graphene.InputObjectType):
    name = graphene.String(required=True)


class AddCoffeeType(graphene.Mutation):
    class Arguments:
        input = AddCoffeeTypeInput(required=True)

    node = graphene.Field(lambda: CoffeeType)

    def mutate(self, info, input):
        coffee_type = CoffeeTypeModel(**input)

        db_session.add(coffee_type)
        db_session.commit()

        return AddCoffeeType(node=coffee_type)


class DeleteCoffeeType(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    id = graphene.ID()

    def mutate(self, info, id):
        querry = (delete(CoffeeTypeModel).where(CoffeeTypeModel.id == id))
        db_session.execute(querry)
        db_session.commit()

        return DeleteCoffeeType(id=id)


class UpdateCoffeeTypeInput(graphene.InputObjectType):
    name = graphene.String()


class UpdateCoffeeType(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        input = UpdateCoffeeTypeInput(required=True)

    node = graphene.Field(lambda: CoffeeType)

    def mutate(self, info, id, input):
        query = (update(CoffeeTypeModel).where(CoffeeTypeModel.id==id).values(**input))

        db_session.execute(query)
        db_session.commit()

        coffee_type = CoffeeType.get_query(info).filter(CoffeeTypeModel.id == id).first()
        
        return UpdateCoffeeType(node=coffee_type)



class CoffeeTypeMutation(graphene.ObjectType):
    add_coffee_type = AddCoffeeType.Field()
    delete_coffee_type = DeleteCoffeeType.Field()
    update_coffee_type = UpdateCoffeeType.Field()
