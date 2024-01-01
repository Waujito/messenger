package io.github.waujito.messenger.api.chat

import org.springframework.data.repository.CrudRepository
import org.springframework.stereotype.Repository
import java.util.*

@Repository
interface ChatRepository : CrudRepository<Chat, UUID> {
    fun getById(id: UUID): Chat
}