        # Create complete unit - FIX: build first, then verify
        unit = StructuredUnit_5D(
            unit_id=f"5d-unit-{int(time.time())}",
            created_at=time.time(),
            layer1=weather2_data,
            layer2=xyo_witness,
            layer3=math_engine,
            layer4=forecast_output,
            layer5=temporal_validation,
            layer1_hash=layer1_hash,
            layer2_hash=layer2_hash,
            layer3_hash=layer3_hash,
            layer4_hash=layer4_hash,
            layer5_hash=layer5_hash,
            unit_hash=unit_hash,
            verified=False,  # Will be set below
        )
        
        # Now verify
        unit.verified = unit.verify()
        self.built_units.append(unit)
        
        return unit
