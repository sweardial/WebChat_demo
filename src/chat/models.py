from django.db import models
from django.conf import settings
# Create your models here.



class RoomChatMessageManager(models.Manager):
	def get_or_create_private_chat(self, user1, user2):
		try:
			try:
				self.room_name = PrivateChatRoom.objects.get(user1=user1, user2=user2)
			except:
				self.room_name = PrivateChatRoom.objects.get(user1=user2, user2=user1)
		except:
			self.room_name = PrivateChatRoom.objects.create(user1=user1, user2=user2)
			self.room_name.save(using=self._db)
		return self.room_name


		
	def by_room(self, room):
		qs = RoomChatMessage.objects.filter(room=room).order_by("id")
		return qs


class PrivateChatRoom(models.Model):
	"""
	A private room for people to chat in.
	"""

	user1              = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user1")
	user2              = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user2")


class RoomChatMessage(models.Model):
	"""
	Chat message created by a user inside a Room
	"""
	user                = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	room                = models.ForeignKey(PrivateChatRoom, on_delete=models.CASCADE)
	timestamp           = models.DateTimeField(auto_now_add=True)
	content             = models.TextField(unique=False, blank=False )

	objects = RoomChatMessageManager()

	def __str__(self):
		return self.content
