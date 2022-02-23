(function(global) {
    const LiteGraph = global.LiteGraph;

    {% for node_type_name, t in node_types.items() %}
    {% set cl = node_type_name.replace("/", "_") %}

    //////////////////////////////////////////////////////////////////////////

    function {{cl}}() {
        {% for slot_name, slot_type_name in t.inputs.items() %}
        this.addInput({{slot_name | tojson}}, {{slot_type_name | tojson}});
        {% endfor %}
        {% for slot_name, slot_type_name in t.outputs.items() %}
        this.addOutput({{slot_name | tojson}}, {{slot_type_name | tojson}});
        {% endfor %}

        this.properties = {
            {% for prop_name, prop in t.properties.items() %}
            {{prop_name}}: {{prop.default_value}},
            {% endfor %}
        };

        {% for prop_name, prop in t.properties.items() %}
        {% if prop.widget_type %}
        this.addWidget({{prop.widget_type | tojson}}, {{prop.label | tojson}}, this.properties.{{prop_name}}, undefined, { property: {{prop_name | tojson}}, {{prop.format_additional_options_js()}} });
        {% endif %}
        {% endfor %}

        {% if t.feedback_type == "image" %}
        this.size = this.computeSize();
        this.size[1] *= 2;
        {% endif %}
    }

    {{cl}}.title = {{t.label | tojson}};
    {{cl}}.desc = "TODO";

    {% if t.feedback_type == "image" %}
    {{cl}}.prototype.onDrawBackground = NodeWithPreview_onDrawBackground;
    {{cl}}.prototype.onProcessingResults = NodeWithPreview_onProcessingResults;
    {% endif %}

    LiteGraph.registerNodeType({{node_type_name | tojson}}, {{cl}});
    {% endfor %}
})(this);
