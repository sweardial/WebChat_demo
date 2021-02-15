from django.shortcuts import render
from .models import RoomChatMessage, PrivateChatRoom, RoomChatMessageManager
from account.models import Account
from django.db.models import Q



def select_chat_room(request, *args, **kwargs):
    context = {}
    recievers1 = PrivateChatRoom.objects.filter(user1=request.user.id).values_list('user2_id', flat=True)
    recievers2 = PrivateChatRoom.objects.filter(user2=request.user.id).values_list('user1_id', flat=True)
    list_of_recievers = [i for i in recievers1] + [i for i in recievers2]
    recievers_accounts = []
    for recievers in list_of_recievers:
        room_no = PrivateChatRoom.objects.get(Q(user1 = request.user.id, user2=recievers) | Q(user1=recievers, user2=request.user.id))
        reciever_account = Account.objects.get(id = recievers)
        if len(RoomChatMessage.objects.filter(room = room_no).values('content')) > 0 :
            recievers_accounts.append((reciever_account.username, reciever_account.id))
    print(recievers_accounts)
    context['list_of_recievers'] = recievers_accounts
    return render(request, 'chat/select_chat.html', context)


def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name,
    })
    


def displaying_messages(request, *args, **kwargs):
    user1 = request.user.id
    user2 = int(kwargs['room_name'].replace(str(user1), ''))
    print(kwargs['room_name'])
    user1_account = Account.objects.get(id=user1)
    user2_account = Account.objects.get(id=user2)
    context = {}
    try:
        try:
            room_id = PrivateChatRoom.objects.get(user1=user1, user2=user2).id
            room = PrivateChatRoom.objects.get(user1=user1, user2=user2)
        except:
            room_id = PrivateChatRoom.objects.get(user1=user2, user2=user1).id
            room = PrivateChatRoom.objects.get(user1=user2, user2=user1)
    except:
        RoomChatMessage.objects.get_or_create_private_chat(user1=user1_account, user2=user2_account)
        room_id = PrivateChatRoom.objects.get(user1=user1, user2=user2).id
        room = PrivateChatRoom.objects.get(user1=user1, user2=user2)

    messages = RoomChatMessage.objects.filter(room=room_id).values_list('content', flat=True)
    senders = RoomChatMessage.objects.filter(room=room_id).values_list('user_id', flat=True)

    recievers1 = PrivateChatRoom.objects.filter(user1=request.user.id).values_list('user2_id', flat=True)
    recievers2 = PrivateChatRoom.objects.filter(user2=request.user.id).values_list('user1_id', flat=True)

    list_of_recievers = [i for i in recievers1] + [i for i in recievers2]
    list_of_messages = [i for i in messages]
    list_of_senders = [i for i in senders]
    final_list = list(zip(list_of_messages, list_of_senders))
    recievers_accounts = []
    for recievers in list_of_recievers:
        room_no = PrivateChatRoom.objects.get(Q(user1 = request.user.id, user2=recievers) | Q(user1=recievers, user2=request.user.id))
        reciever_account = Account.objects.get(id = recievers)
        if len(RoomChatMessage.objects.filter(room = room_no).values('content')) > 0 :
            recievers_accounts.append((reciever_account.username, reciever_account.id))

    context['user1'] = user1
    context['user2'] = user2
    context['room_name'] = kwargs['room_name']
    context['final_list'] = final_list
    context['list_of_recievers'] = recievers_accounts

    return render(request, 'chat/room.html', context)


    
