from joblib import dump


class ModelWriter:

    @staticmethod
    def write_model(model, output_path):
        """
        Write model generated
        :param model: Model to be persisted
        :param output_path: Path to write
        """
        dump(model, output_path)
        return 0
