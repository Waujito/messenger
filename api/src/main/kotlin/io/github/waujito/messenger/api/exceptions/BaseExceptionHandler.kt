package io.github.waujito.messenger.api.exceptions

import org.springframework.http.HttpStatus
import org.springframework.http.ResponseEntity

/**
 * Defines a bunch of default responses for exceptions
 */
open class BaseExceptionHandler {
    /**
     * Responds with status and exception message
     */
    open fun baseHandler(ex: Exception, status: HttpStatus) = ResponseEntity
            .status(status)
            .body(
                    ExceptionResponse(
                            status = status,
                            message = ex.message
                    )
            )

    /**
     * Responds with status, exception message and custom message
     */
    open fun baseHandler(ex: Exception, status: HttpStatus, message: String) = ResponseEntity
            .status(status)
            .body(
                    ExceptionResponse(
                            status = status,
                            error = ex.message,
                            message = message
                    )
            )

    /**
     * Responds with just a status
     */
    open fun baseHandler(status: HttpStatus) = ResponseEntity
            .status(status)
            .body(
                    ExceptionResponse(
                            status = status
                    )
            )
}