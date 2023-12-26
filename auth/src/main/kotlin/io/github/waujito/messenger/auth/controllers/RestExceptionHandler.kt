package io.github.waujito.messenger.auth.controllers

import org.springframework.http.HttpStatus
import org.springframework.http.ResponseEntity
import org.springframework.web.bind.annotation.ExceptionHandler
import org.springframework.web.bind.annotation.RestControllerAdvice
import org.springframework.web.context.request.WebRequest
import org.springframework.web.servlet.mvc.method.annotation.ResponseEntityExceptionHandler

@RestControllerAdvice
class RestExceptionHandler : ResponseEntityExceptionHandler() {
    //    @ExceptionHandler(value = {Exception.class})
    //    protected ResponseEntity<?> handleAuthorizationOauth2Exception(Exception ex){
    //        System.out.println(ex.getMessage());
    //        return new ResponseEntity<>(ex.getMessage(), HttpStatusCode.valueOf(405));
    //    }
    @ExceptionHandler(RuntimeException::class)
    fun handleRuntimeException(e: RuntimeException, request: WebRequest): ResponseEntity<ExceptionResponse> {
        return ResponseEntity
                .status(500)
                .body(ExceptionResponse(HttpStatus.valueOf(500), request.contextPath, e.message))
    }
}