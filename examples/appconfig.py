import tired.ux


def main():
    application_config = tired.ux.ApplicationConfig("testapp")
    application_config.set_field("echo", "hello")
    application_config.sync()


if __name__ == "__main__":
    main()
