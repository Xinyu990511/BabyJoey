# Make sure you install the required packages >>> pip install -r requirements.txt
import torch
from torchtnt.framework.fit import fit
import hydra
from omegaconf import DictConfig

print("Loading BabyJoey core classes under `src`...")
from src.callbacks import Log
from src.data import BabyJoeyDataLoader, BabyJoeyDataset
from src.model import BabyJoeyModel
from src.train import BabyJoeyUnit
from src.utils import BabyJoeyUtil
from src.config.config import BabyJoeyConfig

# load predefined global parameters, see details in config/config.py
print("Loading configurations from `config.py`...")
from src.config.config import (
    BATCH_SIZE,
    LEARNING_RATE,
    WEIGHT_DECAY,
    STEP_SIZE,
    GAMMA
)


@hydra.main(version_base=None, config_name="baby_joey_config")
def main(cfg: BabyJoeyConfig):
    # download/save datasets if not existed, otherwise load tokenised datasets
    print("Preparing training and validation datasets...")
    dataset = BabyJoeyDataset(
        data_path=cfg.data.data_path,                   # hf dataset
        column_name=cfg.data.column_name,               # column of dataset to use as input
        sequence_length=cfg.data.sequence_length,       # max token length of input
        train_file=cfg.data.train_file,                 # path to load/save tokenised training set
        valid_file=cfg.data.valid_file,                 # path to load/save tokenised validation set
        split_ratio=cfg.data.split_ratio,               # split ratio of validation set
        sample_ratio=cfg.data.sample_ratio              # sample ratio of whole dataset
    )
    training_dataset, validation_dataset = dataset.load_or_create_datasets()
    print("Created tokenised training set and tokenised validation set")

    # prepare dataloaders given predefined batch size
    print("Preparing training dataloader and validation dataloader...")
    dataloader = BabyJoeyDataLoader(training_dataset, validation_dataset, BATCH_SIZE)
    training_dataloader, validation_dataloader = dataloader.get_dataloaders()
    print(f"Training dataloader has {len(training_dataloader)} batches, "\
          f"validation dataloader has {len(validation_dataloader)} batches")

    # initialise a model based on predefined model structure
    print("Building a model...")
    # TODO: Load device config from config.py? When to explicitly specify device?
    # TODO: Support more devices later https://pytorch.org/docs/stable/distributed.html
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    # model = BabyJoeyModel(cfg)

    model = BabyJoeyModel(cfg).to(device)
    n_params = BabyJoeyUtil.count_params(model)
    print(f"Initialised a model on device {device} with {n_params} trainable parameters")
    
    # prepare AutoUnit
    print("Preparing for training/evaluation/prediction logic...")
    # TODO: Add comments for AutoUnit
    # TODO: Add rank arguments for DDP later
    # TODO: Based on which functions are implemented, provide more info on what logic will be executed.
    baby_joey_unit = BabyJoeyUnit(
        module=model, 
        device=device,
        lr=LEARNING_RATE, 
        weight_decay=WEIGHT_DECAY, 
        step_size=STEP_SIZE, 
        gamma=GAMMA 
    )
    print("Created training/evaluation/prediction logic")

    # Train and evaluate the model using the defined AutoUnit and Callbacks
    print("Executing training/evaluation/prediction logic...")
    # TODO: Add more helpful print information
    fit(
        baby_joey_unit,  # training AutoUnit in train.py
        train_dataloader=training_dataloader,
        eval_dataloader=validation_dataloader,
        max_epochs=2,  # TODO: Load from config.py
        callbacks=[Log()]
    )
    print("Finished training/evaluation/prediction logic")


if __name__ == "__main__":
    main()
