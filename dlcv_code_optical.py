# -*- coding: utf-8 -*-
"""dlcv-code-optical.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/132cwhC_sUCBU4h2aUmRjQmMROfGrUXPc
"""

from huggingface_hub import login

token = "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"
login(token=token)

! pip install -q \
  diffusers \
  transformers \
  safetensors \
  sentencepiece \
  accelerate \
  bitsandbytes \
  einops \
  mediapy \
  accelerate

!pip install -q git+https://github.com/dangeng/visual_anagrams.git

import gc
import mediapy as mp

import torch
from diffusers import DiffusionPipeline

from visual_anagrams.views import get_views
from visual_anagrams.samplers import sample_stage_1, sample_stage_2
from visual_anagrams.utils import add_args, save_illusion, save_metadata

device = 'cuda'

def im_to_np(im):
  im = (im / 2 + 0.5).clamp(0, 1)
  im = im.detach().cpu().permute(1, 2, 0).numpy()
  im = (im * 255).round().astype("uint8")
  return im


# Garbage collection function to free memory
def flush():
    gc.collect()
    torch.cuda.empty_cache()

from huggingface_hub import login

login()  # This will prompt you to enter your Hugging Face token

from transformers import T5EncoderModel


# T5EncoderModel.from_pretrained("DeepFloyd/IF-I-M-v1.0",subfolder="text_encoder", device_map="auto", load_in_8bit=True, variant="8bit")


text_encoder = T5EncoderModel.from_pretrained(
    "DeepFloyd/IF-I-L-v1.0",
    subfolder="text_encoder",
    device_map="auto",
    variant="fp16",
    torch_dtype=torch.float16,
)

pipe = DiffusionPipeline.from_pretrained(
    "DeepFloyd/IF-I-L-v1.0",
    text_encoder=text_encoder,  # pass the previously instantiated text encoder
    unet=None                   # do not use a UNet here, as it uses too much memory
)
pipe = pipe.to(device)

# Replace the single prompt pair section with this:
prompt_pairs = [
    # Architecture/Nature fusion
    ["an oil painting of a gothic cathedral", "an oil painting of a dense forest"],

    # Abstract/Seasonal
    ["a watercolor painting of autumn leaves", "a watercolor painting of butterflies"],

    # Musical/Nature
    ["an oil painting of musical instruments", "an oil painting of peacocks"],

    # Still life transformation
    ["an oil painting of vintage books and scrolls", "an oil painting of blooming roses"],

    # Urban/Fantasy
    ["a painting of venice canals", "a painting of flying dragons"],

    # Literary/Nature
    ["an ink drawing of an ancient library", "an ink drawing of twisted branches"],

    # Technology/Nature
    ["an oil painting of clockwork mechanisms", "an oil painting of seashells"],

    # Abstract/Concrete
    ["a surreal painting of flowing ribbons", "a surreal painting of dancing figures"]
]

# Create embeddings for all prompt pairs
all_embeddings = []
for prompt_1, prompt_2 in prompt_pairs:
    prompts = [prompt_1, prompt_2]
    prompt_embeds = [pipe.encode_prompt(prompt) for prompt in prompts]
    prompt_embeds, negative_prompt_embeds = zip(*prompt_embeds)
    all_embeddings.append({
        'prompt_embeds': torch.cat(prompt_embeds),
        'negative_prompt_embeds': torch.cat(negative_prompt_embeds),
        'prompts': prompts
    })

# Replace the single prompt pair section with this:
prompt_pairs2 = [

    # Mythological/Natural
    ["an oil painting of a phoenix rising", "an oil painting of a blooming cherry tree"],

    # Ocean/Sky
    ["a watercolor of crashing ocean waves", "a watercolor of northern lights"]
]

# Create embeddings for all prompt pairs
all_embeddings2 = []
for prompt_1, prompt_2 in prompt_pairs2:
    prompts = [prompt_1, prompt_2]
    prompt_embeds = [pipe.encode_prompt(prompt) for prompt in prompts]
    prompt_embeds, negative_prompt_embeds = zip(*prompt_embeds)
    all_embeddings2.append({
        'prompt_embeds': torch.cat(prompt_embeds),
        'negative_prompt_embeds': torch.cat(negative_prompt_embeds),
        'prompts': prompts
    })

# Replace the single prompt pair section with this:
prompt_pairs3 = [


    # Urban/Historical
    ["an oil painting of a modern cityscape", "an oil painting of ancient roman ruins"],

    # Emotional Expressions
    ["an impressionist painting of a laughing child", "an impressionist painting of a carnival scene"]
]

# Create embeddings for all prompt pairs
all_embeddings3 = []
for prompt_1, prompt_2 in prompt_pairs3:
    prompts = [prompt_1, prompt_2]
    prompt_embeds = [pipe.encode_prompt(prompt) for prompt in prompts]
    prompt_embeds, negative_prompt_embeds = zip(*prompt_embeds)
    all_embeddings3.append({
        'prompt_embeds': torch.cat(prompt_embeds),
        'negative_prompt_embeds': torch.cat(negative_prompt_embeds),
        'prompts': prompts
    })

# Replace the single prompt pair section with this:
prompt_pairs4 = [


    # Motion Studies
    ["an oil painting of ballet dancers", "an oil painting of windswept willow trees"],

    # Light/Dark Contrasts
    ["a dramatic painting of a lighthouse in storm", "a dramatic painting of a bonfire at night"],

]

# Create embeddings for all prompt pairs
all_embeddings4 = []
for prompt_1, prompt_2 in prompt_pairs4:
    prompts = [prompt_1, prompt_2]
    prompt_embeds = [pipe.encode_prompt(prompt) for prompt in prompts]
    prompt_embeds, negative_prompt_embeds = zip(*prompt_embeds)
    all_embeddings4.append({
        'prompt_embeds': torch.cat(prompt_embeds),
        'negative_prompt_embeds': torch.cat(negative_prompt_embeds),
        'prompts': prompts
    })

# UNCOMMENT ONE OF THESE

# views = get_views(['identity', 'rotate_180'])
# views = get_views(['identity', 'rotate_cw'])
# views = get_views(['identity', 'rotate_ccw'])
# views = get_views(['identity', 'flip'])
#views = get_views(['identity', 'negate'])
# views = get_views(['identity', 'skew'])
#views = get_views(['identity', 'patch_permute'])
# views = get_views(['identity', 'pixel_permute'])
# views = get_views(['identity', 'inner_circle'])

# views = get_views(['identity', 'square_hinge'])
# views = get_views(['identity', 'jigsaw'])

del text_encoder
del pipe
flush()
flush()   # For some reason we need to do this twice

from diffusers import DiffusionPipeline

# Load DeepFloyd IF stage I
stage_1 = DiffusionPipeline.from_pretrained(
    "DeepFloyd/IF-I-L-v1.0",
    text_encoder=None,
    variant="fp16",
    torch_dtype=torch.float16,
)
stage_1.enable_model_cpu_offload()
stage_1.to(device)
# stage_1.to("cpu")

# Load DeepFloyd IF stage II
stage_2 = DiffusionPipeline.from_pretrained(
                "DeepFloyd/IF-II-L-v1.0",
                text_encoder=None,
                variant="fp16",
                torch_dtype=torch.float16,
              )
stage_2.enable_model_cpu_offload()
stage_2.to(device)

# Load DeepFloyd IF stage III
# (which is just Stable Diffusion 4x Upscaler)
stage_3 = DiffusionPipeline.from_pretrained(
                "stabilityai/stable-diffusion-x4-upscaler",
                torch_dtype=torch.float16
            )
stage_3.enable_model_cpu_offload()
stage_3 = stage_3.to(device)
# stage_3.to("cpu")



"""# Linlin Zhang"""

# Add these imports at the beginning with other imports
import torchvision.transforms.functional as TF
from visual_anagrams.animate import animate_two_view

import gc
import mediapy as mp
import torch
import torchvision.transforms.functional as TF
from diffusers import DiffusionPipeline
from visual_anagrams.views import get_views
from visual_anagrams.samplers import sample_stage_1, sample_stage_2
from visual_anagrams.utils import add_args, save_illusion, save_metadata
from visual_anagrams.animate import animate_two_view

# Add this import at the beginning with other imports
import torchvision.transforms.functional as TF

# After loading the models (stage_1, stage_2, stage_3), add this loop:
# Then continue with the loop code:
for i, embedding in enumerate(all_embeddings):
    print(f"\nGenerating illusion {i+1}/{len(all_embeddings)}")
    print(f"Prompts: {embedding['prompts'][0]} ↔ {embedding['prompts'][1]}")

    # Try different views
    views_types = [
        ['identity', 'rotate_180'],
        ['identity', 'rotate_cw'],
        ['identity', 'flip'],
        ['identity', 'negate']
    ]

    for view_pair in views_types:
        print(f"\nTrying view: {view_pair[1]}")
        views = get_views(view_pair)

        # Generate 64x64
        image_64 = sample_stage_1(stage_1,
                                embedding['prompt_embeds'],
                                embedding['negative_prompt_embeds'],
                                views,
                                num_inference_steps=30,
                                guidance_scale=10.0,
                                reduction='mean',
                                generator=None)

        print("64x64 Result:")
        mp.show_images([im_to_np(view.view(image_64[0])) for view in views])

        # Generate 256x256
        image_256 = sample_stage_2(stage_2,
                                 image_64,
                                 embedding['prompt_embeds'],
                                 embedding['negative_prompt_embeds'],
                                 views,
                                 num_inference_steps=30,
                                 guidance_scale=10.0,
                                 reduction='mean',
                                 noise_level=50,
                                 generator=None)

        print("\n256x256 Result:")
        mp.show_images([im_to_np(view.view(image_256[0])) for view in views])

        # Generate 1024x1024
        image_1024 = stage_3(
                        prompt=embedding['prompts'][0],
                        image=image_256,
                        noise_level=0,
                        output_type='pt',
                        generator=None).images
        image_1024 = image_1024 * 2 - 1


        # # Generate 1024x1024 (with value range correction)
        # image_1024 = stage_3(
        #                 prompt=embedding['prompts'][0],
        #                 image=image_256.clamp(-1, 1),  # Ensure values are in [-1, 1]
        #                 noise_level=0,
        #                 output_type='pt',
        #                 generator=None).images
        # image_1024 = image_1024 * 2 - 1

        print("\n1024x1024 Result:")
        mp.show_images([im_to_np(view.view(image_1024[0])) for view in views], width=400)

        # Create animation
        im_size = image_1024.shape[-1]
        frame_size = int(im_size * 1.5)
        save_video_path = f'./animation_{i}_{view_pair[1]}.mp4'

        pil_image = TF.to_pil_image(image_1024[0] / 2. + 0.5)

        animate_two_view(
            pil_image,
            views[1],
            embedding['prompts'][0],
            embedding['prompts'][1],
            save_video_path=save_video_path,
            hold_duration=120,
            text_fade_duration=10,
            transition_duration=45,
            im_size=im_size,
            frame_size=frame_size,
        )

        print("\nAnimation:")
        mp.show_video(mp.read_video(save_video_path), fps=30, width=min(600, frame_size))

"""# Linlin Zhang 2"""

# UNCOMMENT ONE OF THESE

# views = get_views(['identity', 'rotate_180'])
# views = get_views(['identity', 'rotate_cw'])
# views = get_views(['identity', 'rotate_ccw'])
# views = get_views(['identity', 'flip'])
#views = get_views(['identity', 'negate'])

# views = get_views(['identity', 'skew'])
#views = get_views(['identity', 'patch_permute'])

# views = get_views(['identity', 'pixel_permute'])
# views = get_views(['identity', 'inner_circle'])

# views = get_views(['identity', 'square_hinge'])
# views = get_views(['identity', 'jigsaw'])

# Add these imports at the beginning with other imports
import torchvision.transforms.functional as TF
from visual_anagrams.animate import animate_two_view

import gc
import mediapy as mp
import torch
import torchvision.transforms.functional as TF
from diffusers import DiffusionPipeline
from visual_anagrams.views import get_views
from visual_anagrams.samplers import sample_stage_1, sample_stage_2
from visual_anagrams.utils import add_args, save_illusion, save_metadata
from visual_anagrams.animate import animate_two_view

# Add this import at the beginning with other imports
import torchvision.transforms.functional as TF

# After loading the models (stage_1, stage_2, stage_3), add this loop:
# Then continue with the loop code:
for i, embedding in enumerate(all_embeddings2):
    print(f"\nGenerating illusion {i+1}/{len(all_embeddings2)}")
    print(f"Prompts: {embedding['prompts'][0]} ↔ {embedding['prompts'][1]}")

    # Try different views
    views_types = [
        ['identity', 'skew'],
        ['identity', 'patch_permute']
    ]

    for view_pair in views_types:
        print(f"\nTrying view: {view_pair[1]}")
        views = get_views(view_pair)

        # Generate 64x64
        image_64 = sample_stage_1(stage_1,
                                embedding['prompt_embeds'],
                                embedding['negative_prompt_embeds'],
                                views,
                                num_inference_steps=30,
                                guidance_scale=10.0,
                                reduction='mean',
                                generator=None)

        print("64x64 Result:")
        mp.show_images([im_to_np(view.view(image_64[0])) for view in views])

        # Generate 256x256
        image_256 = sample_stage_2(stage_2,
                                 image_64,
                                 embedding['prompt_embeds'],
                                 embedding['negative_prompt_embeds'],
                                 views,
                                 num_inference_steps=30,
                                 guidance_scale=10.0,
                                 reduction='mean',
                                 noise_level=50,
                                 generator=None)

        print("\n256x256 Result:")
        mp.show_images([im_to_np(view.view(image_256[0])) for view in views])

        # Generate 1024x1024
        image_1024 = stage_3(
                        prompt=embedding['prompts'][0],
                        image=image_256,
                        noise_level=0,
                        output_type='pt',
                        generator=None).images
        image_1024 = image_1024 * 2 - 1


        # # Generate 1024x1024 (with value range correction)
        # image_1024 = stage_3(
        #                 prompt=embedding['prompts'][0],
        #                 image=image_256.clamp(-1, 1),  # Ensure values are in [-1, 1]
        #                 noise_level=0,
        #                 output_type='pt',
        #                 generator=None).images
        # image_1024 = image_1024 * 2 - 1

        print("\n1024x1024 Result:")
        mp.show_images([im_to_np(view.view(image_1024[0])) for view in views], width=400)

        # Create animation
        im_size = image_1024.shape[-1]
        frame_size = int(im_size * 1.5)
        save_video_path = f'./animation_{i}_{view_pair[1]}.mp4'

        pil_image = TF.to_pil_image(image_1024[0] / 2. + 0.5)

        animate_two_view(
            pil_image,
            views[1],
            embedding['prompts'][0],
            embedding['prompts'][1],
            save_video_path=save_video_path,
            hold_duration=120,
            text_fade_duration=10,
            transition_duration=45,
            im_size=im_size,
            frame_size=frame_size,
        )

        print("\nAnimation:")
        mp.show_video(mp.read_video(save_video_path), fps=30, width=min(600, frame_size))

# Add these imports at the beginning with other imports
import torchvision.transforms.functional as TF
from visual_anagrams.animate import animate_two_view

import gc
import mediapy as mp
import torch
import torchvision.transforms.functional as TF
from diffusers import DiffusionPipeline
from visual_anagrams.views import get_views
from visual_anagrams.samplers import sample_stage_1, sample_stage_2
from visual_anagrams.utils import add_args, save_illusion, save_metadata
from visual_anagrams.animate import animate_two_view



# Add this import at the beginning with other imports
import torchvision.transforms.functional as TF

# After loading the models (stage_1, stage_2, stage_3), add this loop:
# Then continue with the loop code:
for i, embedding in enumerate(all_embeddings3):
    print(f"\nGenerating illusion {i+1}/{len(all_embeddings3)}")
    print(f"Prompts: {embedding['prompts'][0]} ↔ {embedding['prompts'][1]}")

    # Try different views
    views_types = [
        ['identity', 'pixel_permute'],
        ['identity', 'inner_circle']
    ]

    for view_pair in views_types:
        print(f"\nTrying view: {view_pair[1]}")
        views = get_views(view_pair)

        # Generate 64x64
        image_64 = sample_stage_1(stage_1,
                                embedding['prompt_embeds'],
                                embedding['negative_prompt_embeds'],
                                views,
                                num_inference_steps=30,
                                guidance_scale=10.0,
                                reduction='mean',
                                generator=None)

        print("64x64 Result:")
        mp.show_images([im_to_np(view.view(image_64[0])) for view in views])

        # Generate 256x256
        image_256 = sample_stage_2(stage_2,
                                 image_64,
                                 embedding['prompt_embeds'],
                                 embedding['negative_prompt_embeds'],
                                 views,
                                 num_inference_steps=30,
                                 guidance_scale=10.0,
                                 reduction='mean',
                                 noise_level=50,
                                 generator=None)

        print("\n256x256 Result:")
        mp.show_images([im_to_np(view.view(image_256[0])) for view in views])

        # Generate 1024x1024
        image_1024 = stage_3(
                        prompt=embedding['prompts'][0],
                        image=image_256,
                        noise_level=0,
                        output_type='pt',
                        generator=None).images
        image_1024 = image_1024 * 2 - 1


        # # Generate 1024x1024 (with value range correction)
        # image_1024 = stage_3(
        #                 prompt=embedding['prompts'][0],
        #                 image=image_256.clamp(-1, 1),  # Ensure values are in [-1, 1]
        #                 noise_level=0,
        #                 output_type='pt',
        #                 generator=None).images
        # image_1024 = image_1024 * 2 - 1

        print("\n1024x1024 Result:")
        mp.show_images([im_to_np(view.view(image_1024[0])) for view in views], width=400)

        # Create animation
        im_size = image_1024.shape[-1]
        frame_size = int(im_size * 1.5)
        save_video_path = f'./animation_{i}_{view_pair[1]}.mp4'

        pil_image = TF.to_pil_image(image_1024[0] / 2. + 0.5)

        animate_two_view(
            pil_image,
            views[1],
            embedding['prompts'][0],
            embedding['prompts'][1],
            save_video_path=save_video_path,
            hold_duration=120,
            text_fade_duration=10,
            transition_duration=45,
            im_size=im_size,
            frame_size=frame_size,
        )

        print("\nAnimation:")
        mp.show_video(mp.read_video(save_video_path), fps=30, width=min(600, frame_size))

# Add these imports at the beginning with other imports
import torchvision.transforms.functional as TF
from visual_anagrams.animate import animate_two_view

import gc
import mediapy as mp
import torch
import torchvision.transforms.functional as TF
from diffusers import DiffusionPipeline
from visual_anagrams.views import get_views
from visual_anagrams.samplers import sample_stage_1, sample_stage_2
from visual_anagrams.utils import add_args, save_illusion, save_metadata
from visual_anagrams.animate import animate_two_view



# Add this import at the beginning with other imports
import torchvision.transforms.functional as TF

# After loading the models (stage_1, stage_2, stage_3), add this loop:
# Then continue with the loop code:
for i, embedding in enumerate(all_embeddings4):
    print(f"\nGenerating illusion {i+1}/{len(all_embeddings4)}")
    print(f"Prompts: {embedding['prompts'][0]} ↔ {embedding['prompts'][1]}")

    # Try different views
    views_types = [
        ['identity', 'square_hinge'],
        ['identity', 'jigsaw']

    ]

    for view_pair in views_types:
        print(f"\nTrying view: {view_pair[1]}")
        views = get_views(view_pair)

        # Generate 64x64
        image_64 = sample_stage_1(stage_1,
                                embedding['prompt_embeds'],
                                embedding['negative_prompt_embeds'],
                                views,
                                num_inference_steps=30,
                                guidance_scale=10.0,
                                reduction='mean',
                                generator=None)

        print("64x64 Result:")
        mp.show_images([im_to_np(view.view(image_64[0])) for view in views])

        # Generate 256x256
        image_256 = sample_stage_2(stage_2,
                                 image_64,
                                 embedding['prompt_embeds'],
                                 embedding['negative_prompt_embeds'],
                                 views,
                                 num_inference_steps=30,
                                 guidance_scale=10.0,
                                 reduction='mean',
                                 noise_level=50,
                                 generator=None)

        print("\n256x256 Result:")
        mp.show_images([im_to_np(view.view(image_256[0])) for view in views])

        # Generate 1024x1024
        image_1024 = stage_3(
                        prompt=embedding['prompts'][0],
                        image=image_256,
                        noise_level=0,
                        output_type='pt',
                        generator=None).images
        image_1024 = image_1024 * 2 - 1


        # # Generate 1024x1024 (with value range correction)
        # image_1024 = stage_3(
        #                 prompt=embedding['prompts'][0],
        #                 image=image_256.clamp(-1, 1),  # Ensure values are in [-1, 1]
        #                 noise_level=0,
        #                 output_type='pt',
        #                 generator=None).images
        # image_1024 = image_1024 * 2 - 1

        print("\n1024x1024 Result:")
        mp.show_images([im_to_np(view.view(image_1024[0])) for view in views], width=400)

        # Create animation
        im_size = image_1024.shape[-1]
        frame_size = int(im_size * 1.5)
        save_video_path = f'./animation_{i}_{view_pair[1]}.mp4'

        pil_image = TF.to_pil_image(image_1024[0] / 2. + 0.5)

        animate_two_view(
            pil_image,
            views[1],
            embedding['prompts'][0],
            embedding['prompts'][1],
            save_video_path=save_video_path,
            hold_duration=120,
            text_fade_duration=10,
            transition_duration=45,
            im_size=im_size,
            frame_size=frame_size,
        )

        print("\nAnimation:")
        mp.show_video(mp.read_video(save_video_path), fps=30, width=min(600, frame_size))









