import adsk.core
import adsk.fusion
import traceback

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface

        # === 使用者輸入：長度 ===
        # inputBox 回傳格式：(輸入的字串, 是否取消)
        result = ui.inputBox('請輸入長度 (cm):', '參數化Box', '10')
        
        # result[1] 才是「是否取消」，如果是 True 代表使用者按了 Cancel
        if result[1]: 
            return
            
        # result[0] 才是「輸入的數值字串」
        length_str = result[0] 
        
        try:
            length = float(length_str)
        except (ValueError, TypeError):
            ui.messageBox(f'長度必須是數字！\n您輸入的是: "{length_str}"')
            return

        # === 使用者輸入：寬度 ===
        result = ui.inputBox('請輸入寬度 (cm):', '參數化Box', '5')
        if result[1]: # 修正這裡
            return
        width_str = result[0] # 修正這裡
        
        try:
            width = float(width_str)
        except (ValueError, TypeError):
            ui.messageBox(f'寬度必須是數字！\n您輸入的是: "{width_str}"')
            return

        # === 使用者輸入：高度 ===
        result = ui.inputBox('請輸入高度 (cm):', '參數化Box', '3')
        if result[1]: # 修正這裡
            return
        height_str = result[0] # 修正這裡
        
        try:
            height = float(height_str)
        except (ValueError, TypeError):
            ui.messageBox(f'高度必須是數字！\n您輸入的是: "{height_str}"')
            return

        # === 驗證數值 ===
        if length <= 0 or width <= 0 or height <= 0:
            ui.messageBox(f'錯誤：所有尺寸必須大於 0！\n目前：長={length}, 寬={width}, 高={height}')
            return

        if length < 0.1 or width < 0.1 or height < 0.1:
            ui.messageBox(f'錯誤：尺寸太小！至少 0.1 cm\n目前：長={length}, 寬={width}, 高={height}')
            return

        # === 建立3D物件 ===
        design = app.activeProduct
        if not design:
            ui.messageBox('錯誤：請先建立新設計 (File → New Design)')
            return
        rootComp = design.rootComponent

        # 建立草圖
        sketches = rootComp.sketches
        xyPlane = rootComp.xYConstructionPlane
        sketch = sketches.add(xyPlane)

        # 畫矩形
        rectangles = sketch.sketchCurves.sketchLines
        point1 = adsk.core.Point3D.create(0, 0, 0)
        point2 = adsk.core.Point3D.create(length, width, 0)
        rectangle = rectangles.addTwoPointRectangle(point1, point2)

        # 擠出
        profile = sketch.profiles.item(0)
        extrudes = rootComp.features.extrudeFeatures
        extInput = extrudes.createInput(
            profile,
            adsk.fusion.FeatureOperations.NewBodyFeatureOperation
        )
        distance = adsk.core.ValueInput.createByReal(height)
        extInput.setDistanceExtent(False, distance)
        extrude = extrudes.add(extInput)

        # 成功！
        ui.messageBox(f'✅ 零件建立完成！\n\n尺寸:\n長度: {length} cm\n寬度: {width} cm\n高度: {height} cm')

    except Exception as e:
        if ui:
            error_msg = f'發生錯誤:\n{str(e)}\n\n詳細資訊:\n{traceback.format_exc()}'
            ui.messageBox(error_msg)

def stop(context):
    pass