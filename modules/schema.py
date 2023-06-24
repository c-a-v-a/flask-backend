from graphene import ObjectType, Schema, relay

from .bean import BeanQuery, BeanMutation
from .coffee_type import CoffeeTypeQuery, CoffeeTypeMutation
from .coffee import CoffeeQuery, CoffeeMutation


class Query(BeanQuery, CoffeeTypeQuery, CoffeeQuery, ObjectType):
    node = relay.Node.Field()
    pass


class Mutation(BeanMutation, CoffeeTypeMutation, CoffeeMutation, ObjectType):
    pass


schema = Schema(query=Query, mutation=Mutation)
