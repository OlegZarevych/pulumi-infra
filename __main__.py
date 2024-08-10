import pulumi
import pulumi_azure_native as azure_native
from pulumi_azure_native import resources
from pulumi_azure_native import storage

resource_group = resources.ResourceGroup("batch-pulumi")

account = storage.StorageAccount(
    "sa",
    resource_group_name=resource_group.name,
    sku=storage.SkuArgs(
        name=storage.SkuName.STANDARD_LRS,
    ),
    kind=storage.Kind.STORAGE_V2,
)


batch_account = azure_native.batch.BatchAccount("batchAccount",
    account_name="bapulumi",
    auto_storage={
        "storage_account_id": account.id,
    },
    
    location=resource_group.location,
    pool_allocation_mode=azure_native.batch.PoolAllocationMode.BATCH_SERVICE,
    resource_group_name=resource_group.name)

pulumi.export("batch_account", batch_account.id.apply(lambda batch_account: batch_account.id))