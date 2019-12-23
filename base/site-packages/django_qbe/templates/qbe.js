{% load i18n %}
/**
 * QBE Interface details
 */
if (!window.qbe) {
    var qbe = {};
}
qbe.Models = {% autoescape off %}{{ json_models }}{% endautoescape %};
{% if json_data %}
qbe.Data = {% autoescape off %}{{ json_data }}{% endautoescape %};
{% else %}
qbe.Data = null;
{% endif %}
qbe.Containers = [];
(function($) {
    $(document).ready(function() {
        var rows = "#qbeConditionsTable tbody tr";

        $("#qbeTabularTab").click(function() {
            selectTab("Tabular");
            return false;
        });
        $("#qbeDiagramTab").click(function() {
            selectTab("Diagram");
            $(window).resize();
            qbe.Diagram.repaintAll();
            return false;
        });
        $("#qbeModelsTab").click(function() {
            // #qbeConnectorList,
            $("#changelist-filter").toggle();
            if ($(".qbeContainer").css("width") == "85%") {
                $(".qbeContainer").css("width", "100%");
            } else {
                $(".qbeContainer").css("width", "85%");
            }
        });
        function selectTab(tab) {
            $("#qbeTabular").hide();
            $("#qbeDiagram").hide();
            $("#qbe"+ tab).show();
        }

        $('#qbeForm tbody tr').formset({
          prefix: '{{ formset.prefix }}',
          addText: '{% trans "Add another" %}',
          addCssClass: "add-row",
          deleteText: '{% trans "Remove" %}',
          deleteCssClass: "inline-deletelink",
          formCssClass: "dynamic-{{ formset.prefix }}",
          emptyCssClass: "add-row",
          removed: qbe.Core.alternatingRows,
          added: qbe.Core.updateRow
        });
        // Workaround in order to get the class "add-row" in the right row
        $(rows +":last").addClass("add-row");

        $("a.qbeModelAnchor").click(qbe.Core.toggleModel);

        $(".submit-row input[type='submit']").click(function() {
            var checked = ($("input[type='checkbox']:checked").length != 0);
            if (!checked) {
                alert("{% trans "Select at least one field to show" %}");
            } else {
                qbe.Diagram.saveBoxPositions();
            }
            return checked;
        });

        $("#autocomplete").click(function() {
            var models = [];
            $(".qbeFillModels :selected").each(function() {
                var key = $(this).val();
                if (models.indexOf(key) == -1) {
                    models.push(key);
                }
            });
            $.ajax({
                url: "{% url django_qbe.views.qbe_autocomplete %}",
                dataType: 'json',
                data: "models="+ models.join(","),
                type: 'post',
                success: showAutocompletionOptions
            });
        });

        function showAutocompletionOptions(data) {
            if (!data) {
                return false;
            }
            var select = $("#autocompletionOptions");
            var options = ['<option disabled="disabled" value="">{% trans "With one of those sets" %}</option>'];
            for(i=0; i<data.length; i++) {
                var key = data[i].join("-");
                var value = data[i].join(", ");
                options.push('<option value="'+ key +'">'+ value +'</option>');
            }
            select.html(options.join(""));
            select.show();
            select.change(function() {
                qbe.Core.addRelationsFrom(select.val());
            });
        };

        $(".qbeFillModels").live("change", qbe.Core.fillModelsEvent);
        $(".qbeFillFields").live("change", qbe.Core.fillFieldsEvent);

        function initialize() {
            if (qbe.Data) {
                qbe.Core.loadData(qbe.Data);
            }
            $(window).resize();
        };
        initialize();
    });
})(jQuery.noConflict());
