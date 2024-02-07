package io.github.waujito.messenger.api.chat.messages

import io.github.waujito.messenger.api.chat.Chat
import io.github.waujito.messenger.api.user.User
import org.springframework.data.domain.Pageable
import org.springframework.stereotype.Service
import java.util.UUID

@Service
class MessageService(val messageRepository: MessageRepository) {
    fun getMessage(messageId: UUID): Message = messageRepository.getById(messageId)


    fun listMessages(chat: Chat, pageable: Pageable): List<RawMessage> {
        val messages = messageRepository.findAllByChatOrderByCreatedAtDesc(chat, pageable)
        return messages.map { RawMessage(it) }
    }

    fun sendMessage(chat: Chat, author: User, content: String): Message {
        val message = Message(chat, author.id, content)
        messageRepository.save(message)

        return message
    }

    fun deleteMessage(message: Message) = messageRepository.delete(message)

    fun updateMessage(message: Message, content: String): Message {
        message.content = content
        messageRepository.save(message)

        return message
    }

    fun assertMessageAuthor(message: Message, author: User): Boolean = message.authorId == author.id
    fun assertMessageChat(message: Message, chat: Chat) = message.chat == chat

}