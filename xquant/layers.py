import tensorflow as tf
from xquant import utils
from xquant import quantizers


class QuantizerBase(tf.keras.layers.Layer):
    def __init__(self, *args, kernel_quantizer=None, input_quantizer=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.kernel_quantizer = quantizers.get(kernel_quantizer)
        self.input_quantizer = quantizers.get(input_quantizer)

    def call(self, inputs):
        if self.kernel_quantizer:
            full_precision_kernel = self.kernel
            self.kernel = self.kernel_quantizer(self.kernel)
        if self.input_quantizer:
            inputs = self.input_quantizer(inputs)

        output = super().call(inputs)
        if self.kernel_quantizer:
            # Reset the full precision kernel to make keras eager tests pass.
            # Is this a problem with our unit tests or a real bug?
            self.kernel = full_precision_kernel
        return output

    def get_config(self):
        config = {
            "kernel_quantizer": quantizers.serialize(self.kernel_quantizer),
            "input_quantizer": quantizers.serialize(self.input_quantizer),
        }
        return {**super().get_config(), **config}


@utils.register_keras_custom_object
class QuantConv1D(QuantizerBase, tf.keras.layers.Conv1D):
    pass


@utils.register_keras_custom_object
class QuantConv2D(QuantizerBase, tf.keras.layers.Conv2D):
    pass


@utils.register_keras_custom_object
class QuantConv3D(QuantizerBase, tf.keras.layers.Conv3D):
    pass


@utils.register_keras_custom_object
class QuantConv2DTranspose(QuantizerBase, tf.keras.layers.Conv2DTranspose):
    pass


@utils.register_keras_custom_object
class QuantConv3DTranspose(QuantizerBase, tf.keras.layers.Conv3DTranspose):
    pass


@utils.register_keras_custom_object
class QuantLocallyConnected1D(QuantizerBase, tf.keras.layers.LocallyConnected1D):
    pass


@utils.register_keras_custom_object
class QuantLocallyConnected2D(QuantizerBase, tf.keras.layers.LocallyConnected2D):
    pass


@utils.register_keras_custom_object
class QuantDense(QuantizerBase, tf.keras.layers.Dense):
    pass
