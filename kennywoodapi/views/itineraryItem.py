"""View module for handling requests about itineraries"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from kennywoodapi.models import Itinerary


class ItinerarySerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for itineraries

    Arguments:
        serializers
    """
    class Meta:
        model = Itinerary
        url = serializers.HyperlinkedIdentityField(
            view_name='itinerary',
            lookup_field='id'
        )
        fields = ('id', 'url', 'starttime', 'attraction',)
        depth = 2


class ItineraryItems(ViewSet):

    def create(self, request):
        new_itinerary_item = Itinerary()
        new_itinerary_item.starttime = request.data["starttime"]
        new_itinerary_item.customer_id = request.auth.user.customer.id
        new_itinerary_item.attraction_id = request.data["attraction_id"]
        new_itinerary_item.save()

        serializer = ItinerarySerializer(new_itinerary_item, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for a single itinerary item

        Returns:
            Response -- JSON serialized itinerary instance
        """
        try:
            itinerary_item = Itinerary.objects.get(pk=pk)
            serializer = ItinerarySerializer(itinerary_item, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to park attractions resource

        Returns:
            Response -- JSON serialized list of park attractions
        """

        itineraries = Itinerary.objects.all()
        serializer = ItinerarySerializer(itineraries, many=True, context={'request': request})

        return Response(serializer.data)

    def update(self, request, pk=None):
      """Handle PUT requests for a itinerary

      Returns:
          Response -- Empty body with 204 status code
      """
      itinerary = Itinerary.objects.get(pk=pk)
      itinerary.starttime = request.data["starttime"]
      itinerary.attraction_id = request.data["attraction_id"]
      itinerary.customer_id = request.data["customer_id"]
      itinerary.save()

      return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single itinerary

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            itinerary = Itinerary.objects.get(pk=pk)
            itinerary.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Itinerary.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

