import threading
import pytest
import json
from time import sleep
from pymilvus import connections
from chaos.checker import (InsertFlushChecker,
                           SearchChecker,
                           QueryChecker,
                           IndexChecker,
                           DeleteChecker,
                           Op)
from common.cus_resource_opts import CustomResourceOperations as CusResource
from utils.util_log import test_log as log
from chaos import chaos_commons as cc
from common.common_type import CaseLabel
from chaos import constants
from delayed_assert import expect, assert_expectations


def assert_statistic(checkers, expectations={}):
    for k in checkers.keys():
        # expect succ if no expectations
        succ_rate = checkers[k].succ_rate()
        total = checkers[k].total()
        average_time = checkers[k].average_time
        if expectations.get(k, '') == constants.FAIL:
            log.info(
                f"Expect Fail: {str(k)} succ rate {succ_rate}, total: {total}, average time: {average_time:.4f}")
            expect(succ_rate < 0.49 or total < 2,
                   f"Expect Fail: {str(k)} succ rate {succ_rate}, total: {total}, average time: {average_time:.4f}")
        else:
            log.info(
                f"Expect Succ: {str(k)} succ rate {succ_rate}, total: {total}, average time: {average_time:.4f}")
            expect(succ_rate > 0.90 and total > 2,
                   f"Expect Succ: {str(k)} succ rate {succ_rate}, total: {total}, average time: {average_time:.4f}")


def get_all_collections():
    try:
        with open("/tmp/ci_logs/all_collections.json", "r") as f:
            data = json.load(f)
            all_collections = data["all"]
    except Exception as e:
        log.error(f"get_all_collections error: {e}")
        return []
    return all_collections


class TestBase:
    expect_create = constants.SUCC
    expect_insert = constants.SUCC
    expect_flush = constants.SUCC
    expect_index = constants.SUCC
    expect_search = constants.SUCC
    expect_query = constants.SUCC
    host = '127.0.0.1'
    port = 19530
    _chaos_config = None
    health_checkers = {}


class TestOperatiions(TestBase):

    @pytest.fixture(scope="function", autouse=True)
    def connection(self, host, port):
        connections.add_connection(default={"host": host, "port": port})
        connections.connect(alias='default')

        if connections.has_connection("default") is False:
            raise Exception("no connections")
        self.host = host
        self.port = port

    def init_health_checkers(self, collection_name=None):
        c_name = collection_name
        checkers = {
            Op.insert: InsertFlushChecker(collection_name=c_name),
            Op.flush: InsertFlushChecker(collection_name=c_name, flush=True),
            Op.index: IndexChecker(collection_name=c_name),
            Op.search: SearchChecker(collection_name=c_name),
            Op.query: QueryChecker(collection_name=c_name),
            Op.delete: DeleteChecker(collection_name=c_name),
        }
        self.health_checkers = checkers

    @pytest.fixture(scope="function", params=get_all_collections())
    def collection_name(self, request):
        if request.param == [] or request.param == "":
            pytest.skip("The collection name is invalid")
        yield request.param

    @pytest.mark.tags(CaseLabel.L3)
    def test_operations(self, collection_name):
        # start the monitor threads to check the milvus ops
        log.info("*********************Test Start**********************")
        log.info(connections.get_connection_addr('default'))
        c_name = collection_name
        self.init_health_checkers(collection_name=c_name)
        cc.start_monitor_threads(self.health_checkers)
        # wait 20s
        sleep(constants.WAIT_PER_OP * 2)
        # assert all expectations
        assert_statistic(self.health_checkers)
        assert_expectations()

        log.info("*********************Chaos Test Completed**********************")
