package io.github.waujito.messenger.api.exceptions.http.client

import io.github.waujito.messenger.api.exceptions.ExceptionResponse
import org.springframework.http.HttpStatus
import org.springframework.http.ResponseEntity
import org.springframework.web.bind.annotation.ExceptionHandler
import org.springframework.web.bind.annotation.RestControllerAdvice

@RestControllerAdvice
class ClientHttpExceptionHandler {
    @ExceptionHandler(NotFoundException::class)
    fun handleNotFound(ex: NotFoundException): ResponseEntity<ExceptionResponse> {
        return ResponseEntity
                .status(404)
                .body(
                        ExceptionResponse(
                                status = HttpStatus.NOT_FOUND,
                                message = ex.message
                        )
                )
    }
    @ExceptionHandler(BadRequestException::class)
    fun handleBadRequest(ex: BadRequestException): ResponseEntity<ExceptionResponse> {
        return ResponseEntity
                .status(400)
                .body(
                        ExceptionResponse(
                                status = HttpStatus.BAD_REQUEST,
                                message = "Bad request",
                                error = ex.message
                        )
                )
    }
}