package io.github.waujito.messenger.api.config

import org.springframework.context.annotation.Configuration
import org.springframework.data.jpa.repository.config.EnableJpaAuditing

@Configuration
@EnableJpaAuditing(modifyOnCreate = false)
class AuditorConfig
