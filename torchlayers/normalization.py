import torch

from ._bases import InferDimension

__all__ = ["InstanceNorm", "BatchNorm", "GroupNorm"]


class _Normalization(InferDimension):
    def __init__(
        self,
        num_features,
        eps=1e-05,
        momentum=0.1,
        affine=True,
        track_running_stats=True,
    ):
        super().__init__(
            module_name=self.module_name(),
            num_features=num_features,
            eps=eps,
            momentum=momentum,
            affine=affine,
            track_running_stats=track_running_stats,
        )


class InstanceNorm(_Normalization):
    """Apply Instance Normalization over inferred dimension (3D up to 5D).

    Based on input shape it either creates 1D, 2D or 3D instance normalization for inputs of shape
    3D, 4D, 5D respectively (including batch as first dimension).

    Otherwise works like standard PyTorch's `InstanceNorm <https://pytorch.org/docs/stable/nn.html#torch.nn.InstanceNorm1d>`__

    Parameters
    ----------
    num_features: int
        :math:`C` (number of channels in input) from an expected input.
        Can be number of outputs of previous linear layer as well
    eps: float, optional
        Value added to the denominator for numerical stability.
        Default: `1e-5`
    momentum: float, optional
        Value used for the `running_mean` and `running_var`
        computation. Default: `0.1`
    affine: bool, optional
        If ``True``, this module has learnable affine parameters, initialized just like in batch normalization.
        Default: ``False``
    track_running_stats: bool, optional
        If ``True``, this module tracks the running mean and variance,
        and when set to ``False``, this module does not track such statistics and always uses batch
        statistics in both training and eval modes.
        Default: ``False``

    """

    def __init__(
        self,
        num_features,
        eps=1e-05,
        momentum=0.1,
        affine=False,
        track_running_stats=False,
    ):
        super().__init__(
            module_name="InstanceNorm",
            num_features=num_features,
            eps=eps,
            momentum=momentum,
            affine=affine,
            track_running_stats=track_running_stats,
        )

    def module_name(self):
        return "InstanceNorm"


class BatchNorm(_Normalization):
    """Apply Batch Normalization over inferred dimension (2D up to 5D).

    Based on input shape it either creates 1D, 2D or 3D batch normalization for inputs of shape
    2D/3D, 4D, 5D respectively (including batch as first dimension).

    Otherwise works like standard PyTorch's `BatchNorm <https://pytorch.org/docs/stable/nn.html#batchnorm1d>`__.

    Parameters
    ----------
    num_features: int
        :math:`C` (number of channels in input) from an expected input.
        Can be number of outputs of previous linear layer as well
    eps: float, optional
        Value added to the denominator for numerical stability.
        Default: `1e-5`
    momentum: float, optional
        Value used for the `running_mean` and `running_var`
        computation. Can be set to ``None`` for cumulative moving average
        (i.e. simple average). Default: `0.1`
    affine: bool, optional
        If ``True``, this module has learnable affine parameters.
        Default: ``True``
    track_running_stats: bool, optional
        If ``True``, this module tracks the running mean and variance,
        and when set to ``False``, this module does not track such statistics and always uses batch
        statistics in both training and eval modes.
        Default: ``True``

    """

    def module_name(self):
        return "BatchNorm"


# Arguments had the wrong order unfortunately
class GroupNorm(torch.nn.GroupNorm):
    """Apply Group Normalization over a mini-batch of inputs.

    Works exactly like PyTorch's counterpart, but `num_channels` is used as first argument
    so it can be inferred during first forward pass.

    Parameters
    ----------

    num_channels: int
        Number of channels expected in input
    num_groups: int
        Number of groups to separate the channels into
    eps: float, optional
        Value added to the denominator for numerical stability.
        Default: `1e-5`
    affine: bool, optional
        If ``True``, this module has learnable affine parameters.
        Default: ``True``

    """

    def __init__(self, num_channels, num_groups, eps=1e-05, affine=True):
        super().__init__(num_groups, num_channels, eps, affine)
