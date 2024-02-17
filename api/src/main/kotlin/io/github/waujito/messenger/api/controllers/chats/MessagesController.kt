package io.github.waujito.messenger.api.controllers.chats

import io.github.waujito.messenger.api.chat.ChatRepository
import io.github.waujito.messenger.api.chat.messages.Message
import io.github.waujito.messenger.api.chat.messages.MessageService
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
class MessagesController(val chatRepository: ChatRepository, val messageService: MessageService) {
    @GetMapping
    fun getMessages(@PathVariable("chatId") chatId: UUID): List<RawMessage> {
        val chat = chatRepository.getById(chatId)

        return messageService.listMessages(chat, Pageable.unpaged())
    }

    @PostMapping
    fun sendMessage(@RequestBody content: String, @PathVariable("chatId") chatId: UUID, authentication: Authentication): ResponseEntity<Message> {
        val chat = chatRepository.getById(chatId)
        val user = authentication.principal as User

        val message = messageService.sendMessage(chat, user, content)

        return ResponseEntity(message, HttpStatus.CREATED)
    }

    @DeleteMapping("{messageId}")
    fun deleteMessage(@PathVariable("chatId") chatId: UUID, @PathVariable("messageId") messageId: UUID): ResponseEntity<Any?> {
        val chat = chatRepository.getById(chatId)
        val message = messageService.getMessage(messageId)

        if (!messageService.assertMessageChat(message, chat)) throw BadRequestException()

        messageService.deleteMessage(message)

        return ResponseEntity(HttpStatus.NO_CONTENT)
    }

    @PutMapping("{messageId}")
    fun deleteMessage(@RequestBody content: String, @PathVariable("chatId") chatId: UUID, authentication: Authentication, @PathVariable("messageId") messageId: UUID): ResponseEntity<Message> {
        val message = messageService.getMessage(messageId)

        val user = authentication.principal as User
        if (!messageService.assertMessageAuthor(message, user)) throw ForbiddenException()

        val chat = chatRepository.getById(chatId)
        if (!messageService.assertMessageChat(message, chat)) throw BadRequestException()

        val newMessage = messageService.updateMessage(message, content)

        return ResponseEntity(newMessage, HttpStatus.NO_CONTENT)
    }
}