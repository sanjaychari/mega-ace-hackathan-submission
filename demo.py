import application
import beaker

def demo() -> None:
    algod_client = beaker.sandbox.get_algod_client()
    accounts = [beaker.sandbox.get_accounts()[-1-i] for i in range(3)]
    app_client = beaker.client.ApplicationClient(
        algod_client, application.app, signer=accounts[0].signer
    )

    # Deploy the app on-chain
    app_id, app_address, _ = app_client.create()
    print(f"Deployed Application ID: {app_id} Address: {app_address}")

    gcphandler = application.GCPHandler()
    gcphandler.setup_accounts(accounts, app_client, signature_threshold=2)
    gcp_service_account_key_path = "/Users/Sanjay/Downloads/aerobic-gift-305004-d7201c4f7998.json"
    gcphandler.create_gcp_vms(requester_address=accounts[0].address, accounts=accounts,
                              gcp_service_account_key_path=gcp_service_account_key_path,
                              signature_threshold=2)

if __name__ == "__main__":
    demo()
