from werkzeug.security import generate_password_hash

print(
    len(
        generate_password_hash(
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAASSASDAUSKDYWDNLQIAAAAAAAAAAAAAAAAAAAAAAAAaaA"
        )
    )
)
