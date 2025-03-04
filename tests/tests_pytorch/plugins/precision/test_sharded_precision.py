# Copyright The PyTorch Lightning team.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pytest
import torch

from pytorch_lightning.overrides.fairscale import _FAIRSCALE_AVAILABLE
from pytorch_lightning.plugins import ShardedNativeMixedPrecisionPlugin
from tests_pytorch.helpers.runif import RunIf

ShardedGradScaler = None
if _FAIRSCALE_AVAILABLE:
    from fairscale.optim.grad_scaler import ShardedGradScaler


@RunIf(fairscale=True)
@pytest.mark.parametrize(
    "precision,scaler,expected",
    [
        (16, torch.cuda.amp.GradScaler(), torch.cuda.amp.GradScaler),
        (16, None, ShardedGradScaler),
        ("bf16", None, None),
        (32, None, None),
    ],
)
def test_sharded_precision_scaler(precision, scaler, expected):
    with pytest.deprecated_call(match="FairScale has been deprecated in v1.9.0"):
        plugin = ShardedNativeMixedPrecisionPlugin(precision=precision, scaler=scaler, device="cuda")
    if expected:
        assert isinstance(plugin.scaler, expected)
    else:
        assert not plugin.scaler
