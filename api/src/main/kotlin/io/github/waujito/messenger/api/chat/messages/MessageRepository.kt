package io.github.waujito.messenger.api.chat.messages

import io.github.waujito.messenger.api.chat.Chat
import org.springframework.data.domain.Pageable
import org.springframework.data.repository.PagingAndSortingRepository
import org.springframework.stereotype.Repository
import java.util.UUID

@Repository
interface MessageRepository: PagingAndSortingRepository<Message, UUID> {
    fun getById(id: UUID): Message

    fun findAllByChat(chat: Chat, pageable: Pageable): List<Message>

    fun findAllByChatAndAuthorId(chat: Chat, authorId: String, pageable: Pageable): List<Message>
//    fun findByChatPaged
}