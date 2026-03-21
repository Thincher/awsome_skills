#!/usr/bin/env python3

import requests
import json
import sys
import os
import time

def load_api_key():
    config_path = os.path.expanduser('~/.openclaw/config/minimax.json')
    
    api_key = os.environ.get('MINIMAX_API_KEY')
    if api_key:
        return api_key
    
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
            return config.get('api_key')
    except (FileNotFoundError, json.JSONDecodeError):
        return None

def text_to_video(prompt, model='MiniMax-Hailuo-2.3', duration=6, resolution='768P', output_file=None):
    api_key = load_api_key()
    if not api_key:
        print("Error: API Key not found. Please configure it first.", file=sys.stderr)
        sys.exit(1)

    url = 'https://api-bj.minimaxi.com/v1/video_generation'
    
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    payload = {
        'model': model,
        'prompt': prompt,
        'prompt_optimizer': True,
        'fast_pretreatment': False,
        'duration': duration,
        'resolution': resolution,
        'aigc_watermark': False
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=120)
        response.raise_for_status()
        
        result = response.json()
        
        if result.get('base_resp', {}).get('status_code') == 0:
            task_id = result.get('task_id')
            if task_id:
                print(f"Video generation task created successfully!")
                print(f"Task ID: {task_id}")
                print(f"\nYou can check task status using task ID.")
                
                if output_file:
                    print(f"\nNote: Video generation is asynchronous. You'll need to poll for result.")
                    print(f"Use task ID to query status and download video when ready.")
                
                return task_id
            else:
                print("Error: No task_id in response", file=sys.stderr)
                sys.exit(1)
        else:
            error_msg = result.get('base_resp', {}).get('status_msg', 'Unknown error')
            print(f"Error: {error_msg}", file=sys.stderr)
            sys.exit(1)
            
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

def image_to_video(first_frame_image, prompt, model='MiniMax-Hailuo-2.3', duration=6, resolution='768P', output_file=None):
    api_key = load_api_key()
    if not api_key:
        print("Error: API Key not found. Please configure it first.", file=sys.stderr)
        sys.exit(1)

    url = 'https://api-bj.minimaxi.com/v1/video_generation'
    
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    payload = {
        'model': model,
        'first_frame_image': first_frame_image,
        'prompt': prompt,
        'prompt_optimizer': True,
        'fast_pretreatment': False,
        'duration': duration,
        'resolution': resolution,
        'aigc_watermark': False
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=120)
        response.raise_for_status()
        
        result = response.json()
        
        if result.get('base_resp', {}).get('status_code') == 0:
            task_id = result.get('task_id')
            if task_id:
                print(f"Image-to-video task created successfully!")
                print(f"Task ID: {task_id}")
                print(f"\nYou can check task status using task ID.")
                
                if output_file:
                    print(f"\nNote: Video generation is asynchronous. You'll need to poll for result.")
                    print(f"Use task ID to query status and download video when ready.")
                
                return task_id
            else:
                print("Error: No task_id in response", file=sys.stderr)
                sys.exit(1)
        else:
            error_msg = result.get('base_resp', {}).get('status_msg', 'Unknown error')
            print(f"Error: {error_msg}", file=sys.stderr)
            sys.exit(1)
            
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

def fl2v_to_video(first_frame_image, last_frame_image, prompt, model='MiniMax-Hailuo-02', duration=6, resolution='768P', output_file=None):
    api_key = load_api_key()
    if not api_key:
        print("Error: API Key not found. Please configure it first.", file=sys.stderr)
        sys.exit(1)

    url = 'https://api-bj.minimaxi.com/v1/video_generation'
    
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    payload = {
        'model': model,
        'first_frame_image': first_frame_image,
        'last_frame_image': last_frame_image,
        'prompt': prompt,
        'prompt_optimizer': True,
        'fast_pretreatment': False,
        'duration': duration,
        'resolution': resolution,
        'aigc_watermark': False
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=120)
        response.raise_for_status()
        
        result = response.json()
        
        if result.get('base_resp', {}).get('status_code') == 0:
            task_id = result.get('task_id')
            if task_id:
                print(f"FL2V task created successfully!")
                print(f"Task ID: {task_id}")
                print(f"\nYou can check task status using task ID.")
                
                if output_file:
                    print(f"\nNote: Video generation is asynchronous. You'll need to poll for result.")
                    print(f"Use task ID to query status and download video when ready.")
                
                return task_id
            else:
                print("Error: No task_id in response", file=sys.stderr)
                sys.exit(1)
        else:
            error_msg = result.get('base_resp', {}).get('status_msg', 'Unknown error')
            print(f"Error: {error_msg}", file=sys.stderr)
            sys.exit(1)
            
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

def s2v_to_video(subject_reference, prompt, model='S2V-01', duration=6, resolution='768P', output_file=None):
    api_key = load_api_key()
    if not api_key:
        print("Error: API Key not found. Please configure it first.", file=sys.stderr)
        sys.exit(1)

    url = 'https://api-bj.minimaxi.com/v1/video_generation'
    
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    payload = {
        'model': model,
        'subject_reference': subject_reference,
        'prompt': prompt,
        'prompt_optimizer': True,
        'aigc_watermark': False
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=120)
        response.raise_for_status()
        
        result = response.json()
        
        if result.get('base_resp', {}).get('status_code') == 0:
            task_id = result.get('task_id')
            if task_id:
                print(f"S2V task created successfully!")
                print(f"Task ID: {task_id}")
                print(f"\nYou can check task status using task ID.")
                
                if output_file:
                    print(f"\nNote: Video generation is asynchronous. You'll need to poll for result.")
                    print(f"Use task ID to query status and download video when ready.")
                
                return task_id
            else:
                print("Error: No task_id in response", file=sys.stderr)
                sys.exit(1)
        else:
            error_msg = result.get('base_resp', {}).get('status_msg', 'Unknown error')
            print(f"Error: {error_msg}", file=sys.stderr)
            sys.exit(1)
            
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

def query_task_status(task_id):
    api_key = load_api_key()
    if not api_key:
        print("Error: API Key not found. Please configure it first.", file=sys.stderr)
        sys.exit(1)

    url = 'https://api-bj.minimaxi.com/v1/query/video_generation'
    
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    payload = {
        'task_id': task_id
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        
        if result.get('base_resp', {}).get('status_code') == 0:
            status = result.get('status')
            file_id = result.get('file_id')
            
            print(f"Task ID: {task_id}")
            print(f"Status: {status}")
            
            if file_id:
                print(f"File ID: {file_id}")
                print(f"Video URL: https://api.minimax.chat/v1/files/retrieve?file_id={file_id}")
            
            return status
        else:
            error_msg = result.get('base_resp', {}).get('status_msg', 'Unknown error')
            print(f"Error: {error_msg}", file=sys.stderr)
            sys.exit(1)
            
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

def download_video(file_id, output_file):
    api_key = load_api_key()
    if not api_key:
        print("Error: API Key not found. Please configure it first.", file=sys.stderr)
        sys.exit(1)

    url = f'https://api.minimax.chat/v1/files/retrieve?file_id={file_id}'
    
    headers = {
        'Authorization': f'Bearer {api_key}'
    }

    try:
        response = requests.get(url, headers=headers, timeout=300)
        response.raise_for_status()
        
        if output_file:
            with open(output_file, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            print(f"Video downloaded successfully to: {output_file}")
        else:
            print(f"Video URL: {url}")
            
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 video.py <prompt|image> [options]", file=sys.stderr)
        print("Options:", file=sys.stderr)
        print("  --model <model>         Model version (default: MiniMax-Hailuo-2.3)", file=sys.stderr)
        print("  --duration <seconds>     Video duration in seconds (default: 6)", file=sys.stderr)
        print("  --resolution <res>       Video resolution: 512P, 720P, 768P, 1080P (default: 768P)", file=sys.stderr)
        print("  --query <task_id>      Query task status by task ID", file=sys.stderr)
        print("  --download <file_id>    Download video by file ID", file=sys.stderr)
        print("  --output <file>         Save video to file (mp4 format)", file=sys.stderr)
        print("  --image <path>         First frame image for I2V (image to video)", file=sys.stderr)
        print("  --last-frame <path>    Last frame image for FL2V (first and last frame to video)", file=sys.stderr)
        print("  --subject <path>       Subject reference image for S2V (subject to video)", file=sys.stderr)
        print("Example:", file=sys.stderr)
        print("  python3 video.py '一只可爱的猫咪在阳光下玩耍'", file=sys.stderr)
        print("  python3 video.py '一只可爱的猫咪在阳光下玩耍' --duration 10 --resolution 1080P", file=sys.stderr)
        print("  python3 video.py --query <task_id>", file=sys.stderr)
        print("  python3 video.py --download <file_id> --output video.mp4", file=sys.stderr)
        print("  python3 video.py --image /path/to/image.jpg '猫咪玩耍'", file=sys.stderr)
        print("  python3 video.py --image /path/to/first.jpg --last-frame /path/to/last.jpg '猫咪玩耍'", file=sys.stderr)
        print("  python3 video.py --subject /path/to/subject.jpg '猫咪玩耍'", file=sys.stderr)
        sys.exit(1)
    
    if '--query' in sys.argv:
        idx = sys.argv.index('--query')
        if idx + 1 < len(sys.argv):
            task_id = sys.argv[idx + 1]
            query_task_status(task_id)
        else:
            print("Error: --query requires a task ID", file=sys.stderr)
            sys.exit(1)
        sys.exit(0)
    
    if '--download' in sys.argv:
        idx = sys.argv.index('--download')
        if idx + 1 < len(sys.argv):
            file_id = sys.argv[idx + 1]
            output_file = None
            if '--output' in sys.argv:
                out_idx = sys.argv.index('--output')
                if out_idx + 1 < len(sys.argv):
                    output_file = sys.argv[out_idx + 1]
            download_video(file_id, output_file)
        else:
            print("Error: --download requires a file ID", file=sys.stderr)
            sys.exit(1)
        sys.exit(0)
    
    prompt_or_image = sys.argv[1]
    model = 'MiniMax-Hailuo-2.3'
    duration = 6
    resolution = '768P'
    output_file = None
    first_frame_image = None
    last_frame_image = None
    subject_reference = None
    
    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == '--model' and i + 1 < len(sys.argv):
            model = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == '--duration' and i + 1 < len(sys.argv):
            duration = int(sys.argv[i + 1])
            i += 2
        elif sys.argv[i] == '--resolution' and i + 1 < len(sys.argv):
            resolution = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == '--output' and i + 1 < len(sys.argv):
            output_file = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == '--image' and i + 1 < len(sys.argv):
            first_frame_image = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == '--last-frame' and i + 1 < len(sys.argv):
            last_frame_image = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == '--subject' and i + 1 < len(sys.argv):
            subject_reference = sys.argv[i + 1]
            i += 2
        else:
            i += 1
    
    if subject_reference:
        if len(sys.argv) < 3:
            print("Error: --subject requires a prompt", file=sys.stderr)
            sys.exit(1)
        prompt = sys.argv[2]
        s2v_to_video(subject_reference, prompt, model, duration, resolution, output_file)
    elif first_frame_image and last_frame_image:
        if len(sys.argv) < 3:
            print("Error: --image and --last-frame require a prompt", file=sys.stderr)
            sys.exit(1)
        prompt = sys.argv[2]
        fl2v_to_video(first_frame_image, last_frame_image, prompt, model, duration, resolution, output_file)
    elif first_frame_image:
        if len(sys.argv) < 3:
            print("Error: --image requires a prompt", file=sys.stderr)
            sys.exit(1)
        prompt = sys.argv[2]
        image_to_video(first_frame_image, prompt, model, duration, resolution, output_file)
    else:
        text_to_video(prompt_or_image, model, duration, resolution, output_file)
