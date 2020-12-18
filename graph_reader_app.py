# trunc8 did this
from PIL import Image
import streamlit as st
import pytesseract

import bisect
import csv
import cv2
import logging
import numpy as np

# Python scripts
import coordinate_mapper, helper_functions, opencv_graph_extraction, label_reader
##

def main():
  st.write("""
           # Automated Graph Reader
           """
           )

  st.write("Query for y-values in simple graphs")
  file = st.file_uploader("Please upload an image file", type=["jpg", "png"])

  if file is None:
    st.text("Waiting for the image file to be uploaded")
  else:
    logging.info("The program is starting...")
    
    # Read file
    pil_image = Image.open(file)
    if pil_image.mode != 'RGB':
      pil_image = pil_image.convert('RGB')
    st.image(pil_image, use_column_width=True)
    color_img = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
    img = cv2.cvtColor(color_img, cv2.COLOR_BGR2GRAY)
    
    # Processing
    trimmed_img = helper_functions.trimWhitespace(img)

    logging.info("Getting X and Y axes...")
    xaxis, yaxis = opencv_graph_extraction.getAxes(trimmed_img)
    logging.info("Done")

    logging.info("Extracting and reading X and Y labels...")
    xcoord, ycoord = label_reader.getLabels(trimmed_img, xaxis, yaxis)
    logging.info("Done")

    # Debug data
    logging.debug("X axis pixels:")
    logging.debug(xaxis)
    logging.debug("")
    logging.debug("Y axis pixels:")
    logging.debug(yaxis)
    logging.debug("")
    logging.debug("X coordinates:")
    logging.debug(xcoord)
    logging.debug("")
    logging.debug("Y coordinates:")
    logging.debug(ycoord)
    logging.debug("")

    # Write to webapp
    st.write("X labels:")
    st.write(list(zip(*xcoord))[1])

    st.write("Y labels:")
    st.write(list(zip(*ycoord))[1])

    st.write("(Kindly double-check that the labels match the above graph)")

    logging.info("Mapping pixels to coordinates...")
    m_y, b_y = coordinate_mapper.mapPixelToCoordinate(ycoord)
    m_x, b_x = coordinate_mapper.mapPixelToCoordinate(xcoord)
    logging.info("Done")

    logging.info("Extracting points in the graph plot...")
    opencv_graph_extraction.extractPlot(trimmed_img, xaxis, yaxis, m_x, b_x, m_y, b_y)
    logging.info("Done")

    st.write("Graph reader program executed successfully!")
    x_input = st.number_input("Enter desired x-value", 0.0)
    submit = st.button('Submit')
    if submit:
      x_csv = []
      y_csv = []
      with open('graph_coordinates.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        for row in csv_reader:
          x_csv.append(float(row[0]))
          y_csv.append(float(row[1]))
      try:
        y_output = 0.5*( float(y_csv[bisect.bisect_left(x_csv, x_input)]) + 
                         float(y_csv[bisect.bisect_right(x_csv, x_input)]) )
        st.write(f"y-value is: {y_output}")
      except IndexError:
        st.write("Input seems out of bounds")


if __name__=='__main__':
  logging.basicConfig(level=logging.DEBUG, format='%(levelname)s %(asctime)s.%(msecs)03d %(message)s', datefmt='%H:%M:%S')
  ## Below is a toggle switch for logging messages
  # logging.disable(sys.maxsize)
  try:
    main()
  except Exception as e:
    logging.debug(f"Exception occurred: {e}")
    st.write("Sorry! The program is unable to process this graph as of now")