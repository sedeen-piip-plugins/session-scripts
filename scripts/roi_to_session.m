function roi_to_session(image_filename, output_filepath, image_size, pixel_size, overlays)
% Writes a series of overlays to a session file
% image_filename: Filename of image on which overlays will be displayed
% output_filepath: Path of session file - should have the same prefix as
% the image_filename, with a session.xml suffix. For example, if the
% image_filename is CMU-1.svs, the output filepath should be
% C:\some\directory\CMU-1.session.xml.
% image_size: The size of image_filename [width, height] in pixels
% pixel_size: The size of the pixels in image_filename [width, height] in
% um.
% overlays: An nx1 cell array containing N overlays. Each overlay is a px2
% array where n is the number of vertices in the polygon. Each row of the
% arrayis an x (column) - y (row) coordinate.


% define overlay parameters
color = '#0000ffff'; % RGBA color code
width = 3;
style = 'Solid';

% define overlay positions
% An overlay is defined as a nx2 array, where n is the number of vertices
% in the polygon. Each row is an x (column) - y (row) coordinate.
% An overlay set is defined as a cell array of these nx2 arrays.


% write the XML document
doc_node = com.mathworks.xml.XMLUtils.createDocument('session');

doc_root = doc_node.getDocumentElement;
doc_root.setAttribute('software', 'roi_to_session.m');
doc_root.setAttribute('version', '0.1.0');

image_root = doc_node.createElement('image');
image_root.setAttribute('identifier', image_filename);
doc_root.appendChild(image_root);

dim_root = doc_node.createElement('dimensions');
dim_root.appendChild(doc_node.createTextNode(sprintf('%d,%d', image_size)));
image_root.appendChild(dim_root);

pixel_size_root = doc_node.createElement('pixel-size');
pixel_size_root.setAttribute('units', 'um');
pixel_size_root.appendChild(doc_node.createTextNode(sprintf('%0.6f,%0.6f', pixel_size)));
image_root.appendChild(pixel_size_root);

overlays_root = doc_node.createElement('overlays');
image_root.appendChild(overlays_root);

for overlay_idx = 1:numel(overlays)
    overlay = overlays{overlay_idx};

    % create graphic node
    graphic_root = doc_node.createElement('graphic');
    graphic_root.setAttribute('type', 'polygon');
    graphic_root.setAttribute('name', sprintf('Overlay %d', overlay_idx));
    graphic_root.setAttribute('description', '');
    overlays_root.appendChild(graphic_root);

    % create pen node
    pen_root = doc_node.createElement('pen');
    pen_root.setAttribute('color', color);
    pen_root.setAttribute('width', sprintf('%d', width));
    pen_root.setAttribute('style', style);
    graphic_root.appendChild(pen_root);

    % create font node
    font_root = doc_node.createElement('font');
    font_root.appendChild(doc_node.createTextNode('Arial;12'));
    graphic_root.appendChild(font_root);

    % create and populate point list node
    point_list_root = doc_node.createElement('point-list');
    graphic_root.appendChild(point_list_root);
    for vertex_idx = 1:size(overlay, 1)
        vertex = overlay(vertex_idx, :);
        point_root = doc_node.createElement('point');
        point_root.appendChild(doc_node.createTextNode(sprintf('%0.6f,%0.6f', vertex)));
        point_list_root.appendChild(point_root);
    end
end

xmlwrite(output_filepath, doc_node)
end






