import beaker
import pyteal as pt
from algosdk import transaction
import google.auth
import uuid
from create_gcp_compute_engine import *
import os

app = beaker.Application("Cloud_Spend_Ledger")

class GCPHandler:

    def setup_accounts(self, accounts, app_client, signature_threshold):
        if len(accounts) <= signature_threshold:
            raise Exception("Number of accounts must be greater than the signature threshold.")
        
        version = 1  # multisig version
        self.msig = transaction.Multisig(
            version,
            signature_threshold,
            [account.address for account in accounts],
        )
        print("Multisig Address: ", self.msig.address())
        app_client.fund(100000, self.msig.address())

    def create_gcp_vms(self, requester_address: pt.abi.Address, accounts: pt.abi.Array, gcp_service_account_key_path: pt.abi.String,
                       signature_threshold: pt.Int):
        """Boots number of VMs mentioned in GCP after verifying the transaction in the multisig account"""
        algod_client = beaker.sandbox.get_algod_client()
        sp = algod_client.suggested_params()

        msig_pay = transaction.PaymentTxn(
            self.msig.address(),
            sp,
            requester_address,
            0,
            close_remainder_to=requester_address,
        )
        msig_txn = transaction.MultisigTransaction(msig_pay, self.msig)

        num_signatures = 0
        for account in accounts:
            if account.address != requester_address:
                msig_txn.sign(account.private_key)
                num_signatures += 1
            if num_signatures == signature_threshold:
                break

        txid = algod_client.send_transaction(msig_txn)
        result = transaction.wait_for_confirmation(algod_client, txid, 4)

        if result['confirmed-round']:
            print("GCP Transaction approved by multisig account. Proceeding with VM creation")
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = gcp_service_account_key_path
            default_project_id = google.auth.default()[1]
            instance_name = "quickstart-" + uuid.uuid4().hex[:10]
            instance_zone = "europe-central2-b"

            newest_debian = get_image_from_family(
                project="debian-cloud", family="debian-10"
            )
            disk_type = f"zones/{instance_zone}/diskTypes/pd-standard"
            disks = [disk_from_image(disk_type, 10, True, newest_debian.self_link)]

            create_instance(default_project_id, instance_zone, instance_name, disks)
        
            print("Created Instance")
