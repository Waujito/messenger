package io.github.waujito.messenger.auth.controllers

import jakarta.servlet.RequestDispatcher
import jakarta.servlet.http.HttpServletRequest
import jakarta.servlet.http.HttpServletResponse
import org.springframework.beans.factory.annotation.Value
import org.springframework.boot.web.error.ErrorAttributeOptions
import org.springframework.boot.web.servlet.error.ErrorAttributes
import org.springframework.boot.web.servlet.error.ErrorController
import org.springframework.http.HttpStatus
import org.springframework.http.ResponseEntity
import org.springframework.web.bind.annotation.RequestMapping
import org.springframework.web.bind.annotation.RestController
import org.springframework.web.context.request.WebRequest

@RestController
class ErrorController(
        private val errorAttributes: ErrorAttributes,

        @Value("\${debug:false}")
        private val debug: Boolean
) : ErrorController {
    companion object {
        const val errorPath = "/error"
    }

    fun getErrorPath() : String{
        return errorPath
    }

    @RequestMapping(value = [errorPath])
    fun error(request: HttpServletRequest, response: HttpServletResponse, webRequest: WebRequest): ResponseEntity<ExceptionResponse> {
        val status: Int =
                request.getAttribute(RequestDispatcher.ERROR_STATUS_CODE)?.toString()?.toInt()
                        ?: response.status

        val errorAttributes = getErrorAttributes(webRequest, debug)

        val message: String =
                request.getAttribute(RequestDispatcher.ERROR_MESSAGE)?.toString()
                        ?: errorAttributes["message"] as String?
                        ?: "An error has occurred."
        val path: String =
                request.getAttribute(RequestDispatcher.ERROR_REQUEST_URI)?.toString()
                        ?: errorAttributes["path"] as String

        val timestamp = errorAttributes["timestamp"].toString()
        val error: Any? = errorAttributes["error"]
        val trace = errorAttributes["trace"] as String?


        val responseBody = ExceptionResponse(
                status= HttpStatus.valueOf(status),
                path=path,
                message=message,
                timestamp=timestamp,
                error=error,
                stackTrace=trace
        )

        return ResponseEntity.status(status)
                .body(responseBody)
    }

    private fun getErrorAttributes(request: WebRequest, includeStackTrace: Boolean): Map<String, Any> {
        var errorAttributeOptions = ErrorAttributeOptions.defaults()

        if (includeStackTrace)
            errorAttributeOptions = errorAttributeOptions.including(ErrorAttributeOptions.Include.STACK_TRACE)

        return errorAttributes.getErrorAttributes(
                request, errorAttributeOptions
        )
    }
}