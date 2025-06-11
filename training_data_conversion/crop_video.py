import cv2

def crop_video(input_video_path, output_video_path, x, y, width, height):
    # Abrir el video de entrada
    cap = cv2.VideoCapture(input_video_path)
    
    # Obtener las propiedades del video
    fps = cap.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    original_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    original_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Asegurarse de que las dimensiones del recorte no excedan las dimensiones originales
    if x + width > original_width or y + height > original_height:
        print(f"Error: El área de recorte excede las dimensiones del video original. {original_width} {original_height}")
        return

    # Crear el objeto para escribir el video recortado
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

    # Leer el video y aplicar el recorte
    while True:
        success, frame = cap.read()
        if not success:
            break

        # Recortar la imagen (ROI)
        cropped_frame = frame[y:y+height, x:x+width]

        # Escribir el frame recortado en el video de salida
        out.write(cropped_frame)

    # Liberar los recursos
    cap.release()
    out.release()
    print(f"✅ Video recortado guardado en: {output_video_path}")

# Definir rutas y parámetros
input_video = r"C:\Users\TeamGranon\Desktop\SIT-AUTO_CLASS\DTG\resident-intruder_automatic_labelling\videos\SIT20-6VT-78-5-2025-01-20 08-47-28.mp4"  # Cambia esta ruta por la ruta de tu video
output_video = r"video_recortado2.mp4"  # Cambia esta ruta por donde deseas guardar el video recortado

x = 241  # Posición X
y = 178  # Posición Y
width = 617  # Ancho del recorte
height = 344  # Alto del recorte

# Llamar a la función
crop_video(input_video, output_video, x, y, width, height)
