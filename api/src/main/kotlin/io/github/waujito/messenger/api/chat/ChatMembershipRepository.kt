package io.github.waujito.messenger.api.chat

import org.springframework.data.domain.Pageable
import org.springframework.data.repository.CrudRepository
import org.springframework.data.repository.PagingAndSortingRepository
import org.springframework.stereotype.Repository
import java.util.*

@Repository
interface ChatMembershipRepository : PagingAndSortingRepository<ChatMembership, UUID>, CrudRepository<ChatMembership, UUID> {
    fun getById(id: UUID): ChatMembership

    fun findAllByUserId(userId: String, pageable: Pageable): List<ChatMembership>

    fun findAllByChat(chat: Chat, pageable: Pageable): List<ChatMembership>

    fun getByChatAndUserId(chat: Chat, userId: String): ChatMembership

}