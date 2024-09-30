from torchtnt.framework.callback import Callback

class WandB(Callback):
    ######################## Training state #########################
    def on_train_start(self, state, unit) -> None:
        print("Training started!")

    def on_train_epoch_start(self, state, unit) -> None:
        print(f"Training epoch {unit.train_progress.num_epochs_completed} started!")

    def on_train_step_start(self, state, unit) -> None:
        current_step = unit.train_progress.num_steps_completed
        print(f"Training step {current_step} started.")

    def on_train_step_end(self, state, unit) -> None:
        if state.train_state and state.train_state.step_output:
            current_loss = state.train_state.step_output[0].item()  # Ensure step_output is valid
            print(f"\rCurrent Loss: {current_loss:.6f}", end="")  # Update in the same line for valid loss
        else:
            # Print the "No valid loss" message on a new line
            print("No valid loss available at this step.")

    def on_train_epoch_end(self, state, unit) -> None:
        print(f"Training epoch {unit.train_progress.num_epochs_completed} ended!")

    def on_train_end(self, state, unit) -> None:
        print("Training ended!")

    ######################## Evaluation state #########################
    def on_eval_start(self, state, unit) -> None:
        print("Evaluation started!")

    def on_eval_epoch_start(self, state, unit) -> None:
        print(f"Evaluation epoch {unit.eval_progress.num_epochs_completed} started!")
    
    def on_eval_step_start(self, state, unit) -> None:
        # Log the start of an evaluation step
        print(f"Evaluation batch {unit.eval_progress.num_steps_completed} started.")

    def on_eval_step_end(self, state, unit) -> None:
        # Log evaluation loss at the end of the step if available
        if state.eval_state and state.eval_state.step_output:
            val_loss = state.eval_state.step_output[0].item()  # Ensure step_output is valid
            print(f"Evaluation Loss: {val_loss:.6f}")
        
            # Log validation loss to wandb
            wandb.log({"val_loss": val_loss})
        else:
            print("No valid evaluation loss available for this step.")

    
    def on_eval_epoch_end(self, state, unit) -> None:
        print(f"Evaluation epoch {unit.eval_progress.num_epochs_completed} ended!")    
    
    def on_eval_end(self, state, unit) -> None:
        print("Evaluation ended!")

    ######################## Exception Handling #########################
    def on_exception(self, state, unit, exc: BaseException) -> None:
        print(f"Exception occurred: {exc}")





# ------------- TODO Items for BabyJoey -------------:
# Training Loss: wandb.log({"train_loss": loss})
# Validation Loss: wandb.log({"val_loss": val_loss})
# Training Accuracy (for classification tasks): wandb.log({"train_accuracy": train_accuracy})
# Validation Accuracy (for classification tasks): wandb.log({"val_accuracy": val_accuracy})
# Perplexity (for language modeling): wandb.log({"perplexity": perplexity})
# Learning Rate: wandb.log({"learning_rate": lr})
# Epoch Number: wandb.log({"epoch": current_epoch})
# Step Number: wandb.log({"step": current_step})
# Gradient Norm: wandb.log({"gradient_norm": grad_norm})
# Optional Items for Transformers:
# Attention Weights/Maps: wandb.log({"attention_maps": attention_weights}) (if you want to visualize attention layers)
# Validation Metrics (e.g., F1, precision, recall for classification tasks):
# python
# Copy code
# wandb.log({
#     "val_f1": f1_score, 
#     "val_precision": precision, 
#     "val_recall": recall
# })
# Sample Predictions: wandb.log({"predictions": sample_predictions})
# Confusion Matrix (for classification tasks): wandb.log({"confusion_matrix": confusion_matrix})
# Throughput (Samples per second): wandb.log({"throughput": samples_per_sec})
# GPU/CPU Utilization: wandb.log({"gpu_usage": gpu_usage, "cpu_usage": cpu_usage})
# Model Checkpoints (e.g., every few epochs): wandb.save('model_checkpoint.pt')
# Tokenization Stats (optional, if interested in tokenization performance): wandb.log({"avg_tokens_per_sample": avg_tokens})
# For Language Models (additional logs):
# Perplexity (for language modeling): wandb.log({"perplexity": perplexity})
# Log Likelihood: wandb.log({"log_likelihood": log_likelihood})
