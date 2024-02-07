package io.github.waujito.messenger.api.controllers.chats

import io.github.waujito.messenger.api.chat.ChatRepository
import io.github.waujito.messenger.api.chat.messages.Message
import io.github.waujito.messenger.api.chat.messages.MessageRepository
import io.github.waujito.messenger.api.chat.messages.RawMessage
import io.github.waujito.messenger.api.exceptions.http.client.BadRequestException
import io.github.waujito.messenger.api.exceptions.http.client.ForbiddenException
import io.github.waujito.messenger.api.user.User
import org.springframework.data.domain.Pageable
import org.springframework.http.HttpStatus
import org.springframework.http.ResponseEntity
import org.springframework.security.core.Authentication
import org.springframework.web.bind.annotation.*
import java.util.*

@RestController
@RequestMapping("/api/chats/{chatId}/messages")
class MessagesController(val chatRepository: ChatRepository, val messageRepository: MessageRepository) {
    @GetMapping
    fun getMessages(@PathVariable("chatId") chatId: UUID): List<RawMessage> {
        val chat = chatRepository.getById(chatId)

        val messages = messageRepository.findAllByChatOrderByCreatedAtDesc(chat, Pageable.unpaged())

        return messages.map { RawMessage(it) }
    }

    @PostMapping
    fun sendMessage(@RequestBody content: String, @PathVariable("chatId") chatId: UUID, authentication: Authentication): ResponseEntity<Any?> {
        val chat = chatRepository.getById(chatId)

        val user = authentication.principal as User
        val userId = user.id

        val message = Message(chat, userId, content)

        messageRepository.save(message)

        return ResponseEntity(HttpStatus.CREATED)
    }

    @DeleteMapping("{messageId}")
    fun deleteMessage(@PathVariable("chatId") chatId: UUID, @PathVariable("messageId") messageId: UUID): ResponseEntity<Any?> {
        val chat = chatRepository.getById(chatId)
        val message = messageRepository.getById(messageId)

        if (message.chat != chat) throw BadRequestException()

        messageRepository.deleteById(messageId)

        return ResponseEntity(HttpStatus.NO_CONTENT)
    }

    @PutMapping("{messageId}")
    fun deleteMessage(@RequestBody content: String, @PathVariable("chatId") chatId: UUID, authentication: Authentication, @PathVariable("messageId") messageId: UUID): ResponseEntity<Any?> {
        val chat = chatRepository.getById(chatId)
        val message = messageRepository.getById(messageId)
        val user = authentication.principal as User
        val userId = user.id

        if (message.chat != chat) throw BadRequestException()
        if (message.authorId != userId) throw ForbiddenException()

        message.content = content

        messageRepository.save(message)

        return ResponseEntity(HttpStatus.NO_CONTENT)
    }
}