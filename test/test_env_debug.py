def test_env_debug():
    import os
    print("[ENV] MONGO_URI =", os.getenv("MONGO_URI"))
    print("[ENV] TEST_ROUTER_IP =", os.getenv("TEST_ROUTER_IP"))
    print("[ENV] TEST_ROUTER_USERNAME =", os.getenv("TEST_ROUTER_USERNAME"))
    print("[ENV] TEST_ROUTER_PASSWORD =", os.getenv("TEST_ROUTER_PASSWORD"))
