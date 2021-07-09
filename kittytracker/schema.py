import graphene
# from graphene_django import DjangoObjectType

import kittytracker.tracker.schema
from graphene_django.debug import DjangoDebug

from graphene_django.rest_framework.mutation import SerializerMutation
from kittytracker.tracker.api.serializers import CareLogSerializer, CatSerializer
from kittytracker.tracker.models import CareLog, Cat


class CreateCat(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        color = graphene.String()

    result = graphene.Boolean()
    cat = graphene.Field(lambda: Cat)

    def mutate(self, info, name):
        cat = Cat(name=name)
        result = True
        return CreateCat(cat=cat, result=result)


class MyMutations(graphene.ObjectType):
    create_cat = CreateCat.Field()


# class MyAwesomeMutation(SerializerMutation):
#     class Meta:
#         serializer_class = CatSerializer


class Query(kittytracker.tracker.schema.Query, graphene.ObjectType):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    debug = graphene.Field(DjangoDebug, name='__debug')
    pass


schema = graphene.Schema(query=Query)
