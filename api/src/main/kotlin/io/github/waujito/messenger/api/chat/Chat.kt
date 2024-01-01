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
    @Size(min = 3, max = 255)
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


    override fun equals(other: Any?): Boolean {
        return super.equals(other)
    }

    override fun hashCode(): Int {
        var result = super.hashCode()
        result = 31 * result + name.hashCode()
        result = 31 * result + (createdAt?.hashCode() ?: 0)
        result = 31 * result + (updatedAt?.hashCode() ?: 0)
        return result
    }
}