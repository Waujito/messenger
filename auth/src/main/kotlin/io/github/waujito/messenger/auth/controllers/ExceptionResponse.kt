package io.github.waujito.messenger.auth.controllers

import com.fasterxml.jackson.annotation.JsonGetter
import com.fasterxml.jackson.annotation.JsonInclude
import org.springframework.http.HttpStatus
import java.time.ZoneId
import java.time.ZonedDateTime
import java.time.format.DateTimeFormatter

class ExceptionResponse(
        private val status: HttpStatus,
        val path: String,
        message: String? = null,
        timestamp: String? = null,
        stackTrace: String? = null
) {
    @JsonGetter
    fun status(): Int = status.value()

    @JsonInclude(JsonInclude.Include.NON_NULL)
    val message: String? = message

    val timestamp = timestamp ?: ZonedDateTime
            .now(ZoneId.of("UTC"))
            .format(DateTimeFormatter.ISO_OFFSET_DATE_TIME)



    @JsonInclude(JsonInclude.Include.NON_NULL)
    private var errors: List<Any>? = null
    @JsonGetter
    fun errors() = errors

    @JsonInclude(JsonInclude.Include.NON_NULL)
    private var error: Any? = null
    @JsonGetter
    fun error() = error

    @JsonInclude(JsonInclude.Include.NON_NULL)
    val stackTrace: String? = stackTrace


    constructor(status: HttpStatus,
                path: String,
                message: String? = null,
                timestamp: String? = null,
                errors: List<Any>?,
                stackTrace: String? = null) :
            this(
                    status, path, message, timestamp, stackTrace
            )
    {
        this.errors = errors
    }

    constructor(status: HttpStatus,
                path: String,
                message: String? = null,
                timestamp: String? = null,
                error: Any?,
                stackTrace: String? = null) :
            this(
                    status, path, message, timestamp, stackTrace
            )
    {
        this.error = error
    }
}