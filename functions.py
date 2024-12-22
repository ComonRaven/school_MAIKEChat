import subprocess
import eel

@eel.expose
def generate_code_from_swagger(spec_file, output_dir):
    try:
        # Swagger CodegenをPythonから実行
        command = [
            "java", 
            "-jar", 
            "swagger-codegen-cli-3.0.19.jar", 
            "generate", 
            "-i", spec_file, 
            "-l", "python",  # 生成する言語はPython
            "-o", output_dir
        ]
        
        result = subprocess.run(command, capture_output=True, text=True)

        if result.returncode == 0:
            return f"Code generated successfully in {output_dir}"
        else:
            return f"Error occurred: {result.stderr}"
    except Exception as e:
        return f"Exception: {str(e)}"