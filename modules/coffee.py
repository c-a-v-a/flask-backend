import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from sqlalchemy import delete

from models.database import db_session
from models.coffee import CoffeeModel, TimeOfDayEnum
from .custom_node import CustomNode


class Coffee(SQLAlchemyObjectType):
    class Meta:
        model = CoffeeModel
        interfaces = ( CustomNode, )


class CoffeeQuery(graphene.ObjectType):
    all_coffee = SQLAlchemyConnectionField(Coffee.connection)


class AddCoffeeInput(graphene.InputObjectType):
    sweetener = graphene.String()
    time_of_day = graphene.String(required=True)
    date = graphene.Date()
    coffee_type_id = graphene.Int(required=True)
    bean_id = graphene.Int(required=True)


class AddCoffee(graphene.Mutation):
    class Arguments:
        input = AddCoffeeInput(required=True)

    coffee = graphene.Field(lambda: Coffee)

    def mutate(self, info, input):
        input.time_of_day = TimeOfDayEnum(input.time_of_day)
        coffee = CoffeeModel(**input)

        db_session.add(coffee)
        db_session.commit()

        return AddCoffee(coffee=coffee)


class DeleteCoffee(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    id = graphene.ID()

    def mutate(self, info, id):
        query = (delete(Coffee).where(CoffeeModel.id == id))
        db_session.execute(query)
        db_session.commit()

        return AddCoffee(id=id)


class CoffeeMutation(graphene.ObjectType):
    add_coffee = AddCoffee.Field()
    delete_coffee = DeleteCoffee.Field()
