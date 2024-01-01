package io.github.waujito.messenger.api.chat

import jakarta.persistence.*
import jakarta.validation.constraints.Size
import org.springframework.data.annotation.CreatedDate
import org.springframework.data.annotation.LastModifiedDate
import org.springframework.data.jpa.domain.AbstractPersistable
import org.springframework.data.jpa.domain.support.AuditingEntityListener
import java.util.*

/**
 * Represents a single chat.
 * The chat is a basic structure where users perform messaging
 */
@Entity
@EntityListeners(AuditingEntityListener::class)
class Chat(name: String) : AbstractPersistable<UUID>() {
    @Column(nullable = false)
    @Size(max=255)
    var name: String = name
        private set

    @CreatedDate
    @Column(nullable = false, updatable = false)
    var createdAt: Date? = null
        private set

    @LastModifiedDate
    @Column(nullable = true, updatable = true)
    var updatedAt: Date? = null
        private set
}