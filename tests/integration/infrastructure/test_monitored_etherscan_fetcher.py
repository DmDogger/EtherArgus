import pytest
from prometheus_client import CollectorRegistry

from infrastructure.etherscan.fetching.concrete_etherscan_fetcher import (
    MonitoredEtherscanFetcher,
)


class TestMonitoredEtherscanFetcher:
    @pytest.mark.asyncio
    async def test_fetching_observes_latency_histogram_on_success(
        self,
        ethereum_address: str,
        metrics_registry: CollectorRegistry,
        monitored_etherscan_fetcher: MonitoredEtherscanFetcher,
    ) -> None:

        await monitored_etherscan_fetcher(address=ethereum_address)

        samples = {
            sample.name: sample.value
            for metric in metrics_registry.collect()
            for sample in metric.samples
        }

        assert samples["sample_histogram_sum"] > 0.0
