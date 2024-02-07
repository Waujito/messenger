package io.github.waujito.messenger.api.user

import com.fasterxml.jackson.module.kotlin.jacksonObjectMapper
import java.net.URI
import java.net.http.HttpClient
import java.net.http.HttpRequest
import java.net.http.HttpResponse

/**
 * Fetches the user from the authentication server
 */
fun fetchAuthenticationServerUser(token: String, userinfoUri: String): ASUser {
    val httpClient = HttpClient.newHttpClient()

    val uri = URI(userinfoUri)
    val request = HttpRequest.newBuilder(uri)
            .header("Authorization", "Bearer $token")
            .build()

    val response = httpClient.send(request, HttpResponse.BodyHandlers.ofString(Charsets.UTF_8))

    val status = response.statusCode()
    val body = response.body()

    val objectMapper = jacksonObjectMapper()


    when (status) {
        200 -> return objectMapper.readValue(body, ASUser::class.java)
        else -> {
            throw Exception(
                    "The authentication server returned an error with status code: $status " +
                            "and body\n$body"
            )
        }
    }
}