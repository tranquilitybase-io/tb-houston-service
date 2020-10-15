class DeploymentStatus:
    def __init__():
        pass
    PENDING = "PENDING"
    STARTED = "STARTED"
    SUCCESS = "SUCCESS"
    RETRY = "RETRY"
    FAILURE = "FAILURE"
    REVOKED = "REVOKED"

if __name__ == "__main__":
    # Unit test
    print(DeploymentStatus.PENDING)
    print(DeploymentStatus.STARTED)
    print(DeploymentStatus.SUCCESS)
    print(DeploymentStatus.RETRY)
    print(DeploymentStatus.FAILURE)
    print(DeploymentStatus.REVOKED)
