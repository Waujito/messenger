package io.github.waujito.messenger.api.controllers.chats

import io.github.waujito.messenger.api.chat.ChatMembershipRepository
import io.github.waujito.messenger.api.chat.ChatRepository
import org.springframework.data.domain.Pageable
import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.PathVariable
import org.springframework.web.bind.annotation.RequestMapping
import org.springframework.web.bind.annotation.RestController
import java.util.*

@RestController
@RequestMapping("/api/chats/{chatId}/members")
class MembersController(val chatRepository: ChatRepository, val chatMembershipRepository: ChatMembershipRepository) {
    @GetMapping
    fun getMembers(@PathVariable("chatId") chatId: UUID): List<String> {
        val chat = chatRepository.getById(chatId)
        val members = chatMembershipRepository.findAllByChat(chat, Pageable.unpaged())
        val membersIds = members.map { it.userId }

        return membersIds
    }
}