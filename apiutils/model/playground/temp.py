import torch
print(torch.__version__)
print(f"Is CUDA supported by this system? \n\
      {torch.cuda.is_available()}")
print(f"CUDA version: {torch.version.cuda}")
  
# Storing ID of current CUDA device
cuda_id = torch.cuda.current_device()
print(f"ID of current CUDA device:\n\
      {torch.cuda.current_device()}")
        
print(f"Name of current CUDA device:\n\
      {torch.cuda.get_device_name(cuda_id)}")