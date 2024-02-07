package io.github.waujito.messenger.api.controllers.chats

import io.github.waujito.messenger.api.chat.Chat
import io.github.waujito.messenger.api.chat.ChatMembership
import io.github.waujito.messenger.api.chat.ChatMembershipRepository
import io.github.waujito.messenger.api.chat.ChatRepository
import io.github.waujito.messenger.api.user.User
import org.springframework.data.domain.PageRequest
import org.springframework.data.domain.Sort
import org.springframework.http.HttpStatus
import org.springframework.http.MediaType
import org.springframework.http.ResponseEntity
import org.springframework.security.core.Authentication
import org.springframework.transaction.annotation.Transactional
import org.springframework.util.MultiValueMap
import org.springframework.web.bind.annotation.*
import java.util.*

@RestController
@RequestMapping("/api/chats")
class ChatController(val chatRepository: ChatRepository, val chatMembershipRepository: ChatMembershipRepository) {

    @GetMapping("{chatId}")
    fun getChat(@PathVariable("chatId") chatId: UUID): Chat {
        return chatRepository.getById(chatId)
    }

    @GetMapping
    fun getUserChats(
            @RequestParam("pageNumber", defaultValue = "0") pageNumber: Int,
            @RequestParam("pageSize", defaultValue = "100") pageSize: Int,
            authentication: Authentication
    ): List<ChatMembership> {
        val user = authentication.principal as User
        val chatMemberships = chatMembershipRepository
                .findAllByUserId(
                        user.id,
                        PageRequest.of(pageNumber, pageSize, Sort.by("joinedAt"))
                )

        return chatMemberships
    }

    @PostMapping(consumes = [MediaType.APPLICATION_FORM_URLENCODED_VALUE])
    @Transactional
    fun createChat(@RequestBody formData: MultiValueMap<String, String>, authentication: Authentication): ResponseEntity<Any?> {
        val user = authentication.principal as User

        val chatName = formData.getFirst("name") ?: ""

        val chat = chatRepository.save(Chat(chatName))
        val chatMembership = chatMembershipRepository.save(ChatMembership(user.id, chat))

        return ResponseEntity(HttpStatus.CREATED)
    }
}