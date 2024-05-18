from drf_spectacular.extensions import OpenApiViewExtension
from drf_spectacular.utils import inline_serializer, extend_schema, extend_schema_field
from rest_framework import serializers
from backend.serializers import OrderSerializer


class StatusOnlySerializer(serializers.Serializer):
    Status = serializers.BooleanField()


class FixRegisterAccount(OpenApiViewExtension):
    target_class = 'backend.views.RegisterAccount'

    def view_replacement(self):

        @extend_schema(
            tags=['Users'],
            summary='Register new account',
            request=inline_serializer(
                name='RegisterAccountRequest',
                fields={
                    'first_name': serializers.CharField(),
                    'last_name': serializers.CharField(),
                    'email': serializers.CharField(),
                    'password': serializers.CharField(),
                    'company': serializers.CharField(),
                    'position': serializers.CharField(),
                },
            ),
            responses={
                (200, 'application/json'): StatusOnlySerializer
            },
        )
        class Fixed(self.target_class):
            pass

        return Fixed


class FixLoginAccount(OpenApiViewExtension):
    target_class = 'backend.views.LoginAccount'

    def view_replacement(self):

        @extend_schema(
            tags=['Users'],
            summary='Login to account',
            request=inline_serializer(
                name='LoginAccountRequest',
                fields={
                    'email': serializers.CharField(),
                    'password': serializers.CharField(),
                },
            ),
            responses={
                (200, 'application/json'): inline_serializer(
                        name='LoginAccountResponseOk',
                        fields={
                            'Status': serializers.BooleanField(),
                            'Token': serializers.CharField(),
                        },
                    ),
            },
        )
        class Fixed(self.target_class):
            pass

        return Fixed


class FixBasketView(OpenApiViewExtension):
    target_class = 'backend.views.BasketView'

    def view_replacement(self):
        
        @extend_schema(
                tags=['Shop'],
                summary='User''s basket',
                responses={
                    (200, 'application/json'): OrderSerializer,
                },
            )
        class Fixed(self.target_class):
            @extend_schema(
                summary='Retrieve the items in the user''s basket',
                responses={
                    (200, 'application/json'): OrderSerializer,
                },
            )
            def get(self, request, *args, **kwargs):
                pass

            @extend_schema(
                summary='Add an item to the user''s basket',
                responses={
                (200, 'application/json'): inline_serializer(
                        name='BasketViewPostOk',
                        fields={
                            'Status': serializers.BooleanField(),
                            'Создано объектов': serializers.CharField(),
                        },
                    ),
            },
            )
            def post(self, request, *args, **kwargs):
                pass

            @extend_schema(
                summary='Update the quantity of an item in the user''s basket',
                responses={
                (200, 'application/json'): inline_serializer(
                        name='BasketViewPutOk',
                        fields={
                            'Status': serializers.BooleanField(),
                            'Создано объектов': serializers.CharField(),
                        },
                    ),
            },
            )
            def put(self, request, *args, **kwargs):
                pass

            @extend_schema(
                summary='Remove an item from the user''s basket',
                responses={
                (200, 'application/json'): inline_serializer(
                        name='BasketViewDeleteOk',
                        fields={
                            'Status': serializers.BooleanField(),
                            'Удалено объектов': serializers.CharField(),
                        },
                    ),
            },
            )
            def delete(self, request, *args, **kwargs):
                pass
        
        return Fixed


class FixPartnerExport(OpenApiViewExtension):
    target_class = 'backend.views.PartnerExport'

    def view_replacement(self):

        @extend_schema(
            tags=['Partner'],
            summary='Export partner price in YAML format',
            responses={
                (200, 'application/json'): inline_serializer(
                        name='PartnerExportResponseOk',
                        fields={
                            'Status': serializers.BooleanField(),
                            'Task_id': serializers.CharField(),
                            'url': serializers.CharField(),
                        },
                    ),
            },
        )
        class Fixed(self.target_class):
            pass

        return Fixed


class FixPartnerOrders(OpenApiViewExtension):
    target_class = 'backend.views.PartnerOrders'

    def view_replacement(self):

        @extend_schema(
            tags=['Partner'],
        )
        class Fixed(self.target_class):
            @extend_schema(
                summary='Retrieve the orders associated with the authenticated partner',
                responses={
                    (200, 'application/json'): OrderSerializer,
                },
            )
            def get(self, request, *args, **kwargs):
                pass
            
            @extend_schema(
                summary='Update the state of an order',
                responses={
                (200, 'application/json'): StatusOnlySerializer
            },
            )
            def put(self, request, *args, **kwargs):
                pass

        return Fixed


class FixResultsView(OpenApiViewExtension):
    target_class = 'backend.views.ResultsView'

    def view_replacement(self):

        class Fixed(self.target_class):
            @extend_schema(
                tags=['Common'],
                summary='Get the result of a task executed asynchronously in Celery',
                request=inline_serializer(
                    name='ResultsViewRequest',
                    fields={
                        'email': serializers.CharField(),
                        'password': serializers.CharField(),
                    },
                ),
                responses={
                    (200, 'application/json'): inline_serializer(
                            name='ResultsViewResponseOk',
                            fields={
                                'Status': serializers.BooleanField(),
                                'Token': serializers.CharField(),
                            },
                        ),
                },
            )
            def get(self, request, *args, **kwargs):
                pass

        return Fixed
