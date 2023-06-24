import graphene


class CustomNode(graphene.Node):
    class Meta:
        name = 'mNode'

    @staticmethod
    def to_global_id(type, id):
        return id
