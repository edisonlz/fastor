if (!window.qbe) {
    var qbe = {};
}
qbe.CurrentModels = [];
qbe.CurrentRelations = [];
qbe.Core = function() {};

(function($) {
    $(document).ready(function() {
        /**
         * Handle the loading initial data blocking process
         */
        var _loadingData = false;

        /**
         * Load initial data to edit query
         */
        qbe.Core.loadData = function(data) {
            var initialForms, maxForms, totalForms;
            _loadingData = true;
            initialForms = parseInt(data["form-INITIAL_FORMS"]);
            maxForms = parseInt(data["form-MAX_NUM_FORMS"]);
            totalForms = parseInt(data["form-TOTAL_FORMS"]);
            for(var i=initialForms; i<totalForms; i++) {
                var appModel, splits, show, model, field, sorted;
                appModel = data["form-"+ i +"-model"];
                if (!(appModel in qbe.CurrentModels)) {
                    splits = appModel.split(".");
                    app = splits[0];
                    model = splits[1];
                    qbe.Core.addModule(app, model);
                }
                qbe.Core.updateModels();
                $("#id_form-"+ i +"-model").val(appModel);
                $("#id_form-"+ i +"-model").change();
                field = data["form-"+ i +"-field"];
                $("#id_form-"+ i +"-field").val(field);
                $("#id_form-"+ i +"-field").change();
                sorted = data["form-"+ i +"-sort"];
                $("#id_form-"+ i +"-sort").val(sorted);
                $("#id_form-"+ i +"-show").remove("checked");
                if (data["form-"+ i +"-show"]) {
                    show = data["form-"+ i +"-show"];
                    if (show && show == "on") {
                        $("#id_form-"+ i +"-show").attr("checked", "checked");
                    }
                }
                c = 0;
                criteria = data["form-"+ i +"-criteria_"+ c];
                while(criteria) {
                    $("#id_form-"+ i +"-criteria_"+ c).val(criteria);
                    criteria = data["form-"+ i +"-criteria_"+ ++c];
                }
            }
            $("#id_form_limit").val(data["limit"]);
            var positions, positionSplits, splits, appModel, appName, modelName;
            positions = data["positions"].split("|");
            for(var i=0; i<positions.length; i++) {
                splits = positions[i].split("@");
                appModel = splits[0].split(".");
                appName = appModel[0];
                modelName = appModel[1];
                positionSplits = splits[1].split(";");
                if (!(appModel in qbe.CurrentModels)) {
                    $("#qbeModelItem_"+ modelName).toggleClass("selected");
                    qbe.Core.addModule(appName, modelName);
                }
                $("#qbeBox_"+ modelName).css({
                    left: positionSplits[0],
                    top: positionSplits[1]
                });
            }
            $("#id_positions").val(data["positions"]);
            _loadingData = false;
        };

        /**
         * Toggle visibility of models
         */
        qbe.Core.toggleModel = function () {
            var id, appName, modelName, idSplits, splits, $this;
            $this = $(this);
            idSplits = $this.attr("id").split("qbeModelAnchor_");
            splits = idSplits[1].split(".");
            appName = splits[0];
            modelName = splits[1];
            $("#qbeModelItem_"+ modelName).toggleClass("selected");
            if ($("#qbeModelItem_"+ modelName).hasClass("selected")) {
                qbe.Core.addModule(appName, modelName);
            } else {
                qbe.Core.removeModule(appName, modelName);
            }
            qbe.Core.updateModels();
            return false;
        }

        /**
         * Invokes the update of the each row
         */
        qbe.Core.updateModels = function() {
            $(this).each(qbe.Core.updateRow);
        };

        /**
         * Update the rows with the new models added
         */
        qbe.Core.updateRow = function(row) {
            var options = ['<option value="">----</option>'];
            for(i=0; i<qbe.CurrentModels.length; i++) {
                var appModel = qbe.CurrentModels[i];
                var key = appModel;
                var value = appModel.replace(".", ": ");
                options.push('<option value="'+ key +'">'+ value +'</option>');
            }
            $(".qbeFillModels").each(function() {
                var val = $(this).val();
                $(this).html(options.join(""));
                $(this).val(val);
            });
            qbe.Core.alternatingRows();
        };

        /**
         * Set a CSS class for alterned rows
         */
        qbe.Core.alternatingRows = function() {
            var rows = "#qbeConditionsTable tbody tr";
            $(rows).not(".add-row").removeClass("row1 row2");
            $(rows +":even").not(".add-row").addClass("row1");
            $(rows +":odd").not(".add-row").addClass("row2");
            $(rows +":last").addClass("add-row");
        };

        /**
         * Add rows per new relation with the models list hyphen separated
         */
        qbe.Core.addRelationsFrom = function(through) {
            var appModels
            appModels = through.split("-");
            for(var i=0; i<appModels.length; i++) {
                var appModel = appModels[i];
                var splits = appModel.split(".");
                qbe.Core.addModule(splits[0], splits[1]);
                $("#qbeModelItem_"+ splits[1]).addClass("selected");
                $("#qbeForm .add-row").click();
                $(".qbeFillModels:last").val(splits[0] +"."+ splits[1]);
                $(".qbeFillModels:last").change();
                $(".qbeFillFields:last").val(splits[2]);
                $(".qbeFillFields:last").change();
            }
        };

        /**
         * Event triggered when the SELECT tag for fill models is changed
         */
        qbe.Core.fillModelsEvent = function() {
            var appModel, key, fields, splits, appModelSplits, prefix, css, cssSplit, domTo, option, optFields, optPrimaries, optForeigns, optManies, style, value;
            appModel = $(this).val();
            if (appModel) {
                appModelSplits = appModel.split(".");
                fields = qbe.Models[appModelSplits[0]][appModelSplits[1]].fields;
                splits = $(this).attr("id").split("-");
                prefix = splits.splice(0, splits.length-1).join("-");
                css = $(this).attr("class");
                cssSplit = css.split("to:")
                domTo = prefix +"-"+ cssSplit[cssSplit.length-1];
                optFields = [];
                optPrimaries = [];
                optForeigns = [];
                optManies = [];
                for(key in fields) {
                    // We can't jump fields with no target 'cause they are
                    // ManyToManyField and ForeignKey fields!
                    value = fields[key].label;
                    if (fields[key].type == "ForeignKey") {
                        style = "foreign";
                        option = '<option class="'+ style +'" value="'+ key +'">'+ value +'</option>'
                        optForeigns.push(option);
                    } else if (fields[key].type == "ManyToManyField") {
                        style = "many";
                        option = '<option class="'+ style +'" value="'+ key +'">'+ value +'</option>'
                        optManies.push(option);
                    } else if (fields[key].primary) {
                        style = "primary";
                        option = '<option class="'+ style +'" value="'+ key +'">'+ value +'</option>'
                        optPrimaries.push(option);
                    } else {
                        style = "";
                        option = '<option class="'+ style +'" value="'+ key +'">'+ value +'</option>'
                        optFields.push(option);
                    }
                }
                $("#"+ domTo).html('<option value="">*</option>' + optPrimaries.join("") + optForeigns.join("") + optManies.join("") + optFields.join(""));
                // We need to raise change event
                $("#"+ domTo).change();
            }
        };

        /**
         * Event triggered when the SELECT tag for fill fields is changed
         */
        qbe.Core.fillFieldsEvent = function() {
            var field, splits, prefix, css, cssSplit, inputs, input, domTo, appModel, appModelSplits, fields, primary, target, targetRel, targetModel, targetStrings, targetString, relations;
            field = $(this).val();
            splits = $(this).attr("id").split("-");
            prefix = splits.splice(0, splits.length-1).join("-");
            css = $(this).attr("class");
            cssSplit = css.split("enable:")
            inputs = cssSplit[cssSplit.length-1].split(",");
            for(var i=0; i<inputs.length; i++) {
                input = inputs[i];
                domTo = prefix +"-"+ input;
                if (field) {
                    $("#"+ domTo).removeAttr("disabled");
                } else {
                    $("#"+ domTo).attr("disabled", "disabled");
                    $("#"+ domTo).val("");
                }
                if ($("#"+ domTo).is('input[type="text"]')) {
                    appModel = $("#"+ prefix +"-model").val();
                    appModelSplits = appModel.split(".");
                    fields = qbe.Models[appModelSplits[0]][appModelSplits[1]].fields;
                    if (field in fields && fields[field].target && !_loadingData) {
                        target = fields[field].target;
                        if (target.through) {
                            $(this).parent().parent().children("td:last").children("a").click();
                            targetModel = qbe.Models[target.through.name][target.through.model];
                            targetsString = [];
                            relations = targetModel.relations;
                            for(var r=0; r<targetModel.relations.length; r++) {
                                targetRel = targetModel.relations[r];
                                targetString = target.through.name +"."+ target.through.model +"."+ targetRel.source;
                                targetsString.push(targetString);
                            }
                            qbe.Core.addRelationsFrom(targetsString.join("-"));
                        } else {
                            targetString = target.name +"."+ target.model +"."+ target.field;
                            $("#"+ domTo).val(targetString);
                            $("#"+ domTo).prev().val("join");
                            qbe.Core.addRelationsFrom(targetString);
                        }
                    } else {
                        $("#"+ domTo).val("");
                    }
                }
            }
        };

        /**
         * Adds a model to the layer
         */
        qbe.Core.addModule = function (appName, modelName) {
            var appModel, model, target1, target2;
            model = qbe.Models[appName][modelName];
            appModel = appName +"."+ modelName;
            if (qbe.CurrentModels.indexOf(appModel) < 0) {
                qbe.CurrentModels.push(appModel);
                if (model.is_auto) {
                    target1 = model.relations[0].target;
                    target2 = model.relations[1].target;
                    qbe.Core.addModule(target1.name, target1.model);
                    qbe.Core.addModule(target2.name, target2.model);
                } else {
                    qbe.Diagram.addBox(appName, modelName);
                }
                qbe.Core.updateRelations();
            }
        };

        /*
         * Removes a model from the layer
         */
        qbe.Core.removeModule = function(appName, modelName) {
            var appModel = appName +"."+ modelName;
            var pos = qbe.CurrentModels.indexOf(appModel);
            if (pos >= 0) {
                qbe.CurrentModels.splice(pos, 1);
                var model = qbe.Models[appName][modelName];
                qbe.Diagram.removeBox(appName, modelName)
                qbe.Diagram.removeRelations(appName, modelName);
            }
        };

        /*
         * Update relations among models
         */
        qbe.Core.updateRelations = function () {
            var label, labelStyle, paintStyle, backgroundPaintStyle, makeOverlay;
            var relations, relation, mediumHeight, connections;
            var sourceAppModel, sourceModelName, sourceAppName, sourceModel, sourceFieldName, sourceId, sourceField, sourceSplits, divSource;
            var targetModel, targetAppName, targetModelName, targetFieldName, targetId, targetField, divTarget;
            for(var i=0; i<qbe.CurrentModels.length; i++) {
                sourceAppModel = qbe.CurrentModels[i];
                sourceSplits = sourceAppModel.split(".");
                sourceAppName = sourceSplits[0];
                sourceModelName = sourceSplits[1];
                sourceModel = qbe.Models[sourceAppName][sourceModelName];
                relations = sourceModel.relations;
                for(var j=0; j<relations.length; j++) {
                    relation = relations[j];
                    sourceFieldName = relation.source;
                    label = qbe.Diagram.Defaults["foreign"].label;
                    labelStyle = qbe.Diagram.Defaults["foreign"].labelStyle;
                    paintStyle = qbe.Diagram.Defaults["foreign"].paintStyle;
                    makeOverlays = qbe.Diagram.Defaults["foreign"].makeOverlays;
                    backgroundPaintStyle = qbe.Diagram.Defaults["foreign"].backgroundPaintStyle;
                    if (relation.target.through) {
                        if (qbe.Models[relation.target.through.name][relation.target.through.model].is_auto) {
                            targetModel = relation.target;
                            label = relation.target.through.model;
                            labelStyle = qbe.Diagram.Defaults["many"].labelStyle;
                            paintStyle = qbe.Diagram.Defaults["many"].paintStyle;
                            makeOverlays = qbe.Diagram.Defaults["many"].makeOverlays;
                            backgroundPaintStyle = qbe.Diagram.Defaults["many"].backgroundPaintStyle;
                        } else {
                            targetModel = relation.target.through;
                        }
                    } else {
                        targetModel = relation.target;
                    }
                    targetAppName = targetModel.name;
                    targetModelName = targetModel.model;
                    targetFieldName = targetModel.field;
                    sourceField = $("#qbeBoxField_"+ sourceAppName +"\\."+ sourceModelName +"\\."+ sourceFieldName);
                    targetField = $("#qbeBoxField_"+ targetAppName +"\\."+ targetModelName +"\\."+ targetFieldName);
                    if (sourceField.length && targetField.length
                        && !qbe.Diagram.hasConnection(sourceField, targetField)) {
                        sourceId = "qbeBox_"+ sourceModelName;
                        targetId = "qbeBox_"+ targetModelName;
                        divSource = document.getElementById(sourceId);
                        divTarget = document.getElementById(targetId);
                        if (divSource && divTarget) {
                            qbe.Diagram.addRelation(sourceId, sourceField, targetId, targetField, label, labelStyle, paintStyle, backgroundPaintStyle, makeOverlays());
                        }
                    }
                }
            }
        }

    });
})(jQuery.noConflict());
