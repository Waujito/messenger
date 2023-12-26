import org.jetbrains.kotlin.gradle.tasks.KotlinCompile
import org.springframework.boot.gradle.tasks.bundling.BootJar

plugins {
	id("org.springframework.boot") version "3.2.1"
	id("io.spring.dependency-management") version "1.1.4"
	kotlin("jvm") version "1.9.21"
	kotlin("plugin.spring") version "1.9.21"
  	kotlin("plugin.jpa") version "1.9.21"
	application
	java
}

group = "io.github.waujito.messenger"
version = "0.0.1-SNAPSHOT"

java {
	sourceCompatibility = JavaVersion.VERSION_17
}

repositories {
	mavenCentral()
}

dependencies {
	implementation("org.springframework.boot:spring-boot-starter-data-jpa")
  	runtimeOnly("org.postgresql:postgresql")
  
	implementation("org.springframework.boot:spring-boot-starter-oauth2-resource-server")
	implementation("org.springframework.boot:spring-boot-starter-web")
	implementation("com.fasterxml.jackson.module:jackson-module-kotlin")
	implementation("org.jetbrains.kotlin:kotlin-reflect")
	developmentOnly("org.springframework.boot:spring-boot-devtools")
	testImplementation("org.springframework.boot:spring-boot-starter-test")
}

tasks.withType<KotlinCompile> {
	kotlinOptions {
		freeCompilerArgs += "-Xjsr305=strict"
		jvmTarget = "17"
	}
}

tasks.withType<Test> {
	useJUnitPlatform()
}

application {
	mainClass.set("io.github.waujito.messenger.api.ApiApplicationKt")

}

tasks.jar {
	manifest {
		attributes("Main-Class" to application.mainClass)
	}
}

tasks.named<BootJar>("bootJar") {
	classpath(configurations["developmentOnly"])
}
