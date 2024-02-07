package io.github.waujito.messenger.api.chat.messages

import io.github.waujito.messenger.api.chat.Chat
import org.springframework.data.domain.Pageable
import org.springframework.data.repository.CrudRepository
import org.springframework.data.repository.PagingAndSortingRepository
import org.springframework.stereotype.Repository
import java.util.*

@Repository
interface MessageRepository : PagingAndSortingRepository<Message, UUID>, CrudRepository<Message, UUID> {
    fun getById(id: UUID): Message

    fun findAllByChatOrderByCreatedAtDesc(chat: Chat, pageable: Pageable): List<Message>

    fun findAllByChatAndAuthorIdOrderByCreatedAtDesc(chat: Chat, authorId: String, pageable: Pageable): List<Message>
}